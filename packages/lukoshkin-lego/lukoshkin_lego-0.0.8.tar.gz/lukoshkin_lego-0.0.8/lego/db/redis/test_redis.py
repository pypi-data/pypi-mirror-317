import asyncio

import pytest
import pytest_asyncio

RETENTION_TIME = 3
CTX_ID = "φeta is a ChEeSe%$!"
CTX_ID_AUTOCREATE = "123"


async def _reset_ctx(ctx):
    await ctx.init()
    await ctx.delete()
    await ctx.init()


@pytest.fixture
def ctx():
    ctx_id = "φeta is a ChEeSe%$!"
    return RedisContext(ctx_id, RedisConnection())


@pytest.fixture
def ctx_autocreate():
    ctx_id = "123"
    return RedisContext(
        ctx_id,
        RedisConnection(),
        create_parents_on_set=True,
    )


@pytest_asyncio.fixture(autouse=True)
async def setup_and_cleanup(ctx, ctx_autocreate):
    await _reset_ctx(ctx)
    await _reset_ctx(ctx_autocreate)
    yield
    await ctx.close()
    await ctx_autocreate.close()


@pytest.mark.asyncio
async def test_clean_state(ctx):
    assert await ctx.redon.get(ctx.ctx_id, "$") == [{}]


@pytest.mark.asyncio
async def test_get_missing_key(ctx):
    key = "some"
    assert await ctx.get(key) is None
    with pytest.raises(KeyError) as exc:
        await ctx.get(key, throw_error_if_missing=True)
        assert "Missing parent" in str(exc.value)


@pytest.mark.asyncio
async def test_simple_set_get(ctx):
    await ctx.set_("key", "value")
    assert await ctx.get("key") == "value"
    assert await ctx.get("$.key") == "value"

    await ctx.set_("key", "another_value", prefix="$")
    assert await ctx.get("key", prefix="$") == "another_value"
    assert await ctx.get("key") == "another_value"

    ## TODO: test just `_prefix_key` and `verify_key_path` functions
    with pytest.raises(ValueError, match="Key cannot start with"):
        await ctx.set_("$key", "value")

    with pytest.raises(ValueError, match="Malformed key"):
        await ctx.set_(".key", "value")

    with pytest.raises(ValueError, match="Malformed key"):
        await ctx.set_("key.", "value")

    with pytest.raises(ValueError, match="Malformed key"):
        await ctx.set_("double..dot", "value")

    with pytest.raises(ValueError, match="Malformed key"):
        await ctx.get("$.$.key")

    key = "some-key"
    await ctx.set_(key, key)
    assert await ctx.get(key) == key

    with pytest.raises(ValueError, match="Key must be ASCII"):
        await ctx.set_("φeta", "value")
    with pytest.raises(ValueError, match="Key must have identifier+"):
        await ctx.set_("f eta", "value")


@pytest.mark.asyncio
async def test_set_expiration_time(ctx):
    assert await ctx.ctx_ttl() == -1
    await ctx.set_("key", "value")
    assert await ctx.get("key") == "value"
    await asyncio.sleep(RETENTION_TIME)
    assert await ctx.get("key") == "value"

    await ctx.set_expiration_time(RETENTION_TIME)
    assert await ctx.ctx_ttl() == RETENTION_TIME
    await asyncio.sleep(RETENTION_TIME)
    assert await ctx.get("key") is None
    assert await ctx.ctx_ttl() == -2


@pytest.mark.asyncio
async def test_list_append(ctx):
    await ctx.set_("key", "value", list_append=True)
    assert await ctx.get("key") == ["value"]

    await ctx.set_("key", "value", list_append=True)
    assert await ctx.get("key") == ["value", "value"]

    await ctx.set_("key", "another_value", list_append=True)
    assert await ctx.get("key") == ["value", "value", "another_value"]

    await ctx.set_("another_key", "value")
    with pytest.raises(ValueError) as exc:
        await ctx.set_("another_key", "value", list_append=True)
        assert "Not a list" in str(exc.value)


@pytest.mark.asyncio
async def test_count(ctx):
    assert await ctx.count("key") == 1
    assert await ctx.count("key") == 2
    assert await ctx.count("key") == 3


@pytest.mark.asyncio
async def test_set_get_with_parents(ctx, ctx_autocreate):
    key = "a.b.c"
    value = "value"
    await ctx_autocreate.set_(key, value, create_parents=True)
    assert await ctx_autocreate.get(key) == value

    with pytest.raises(ValueError, match="Malformed prefix"):
        await ctx_autocreate.set_(key, value, prefix="p.q.")

    with pytest.raises(ValueError, match="Key cannot start with"):
        await ctx_autocreate.set_("$invalid.key", value)

    with pytest.raises(KeyError, match="Missing parent"):
        await ctx.set_(key, value)

    await ctx.set_(key, value, create_parents=True)
    assert await ctx_autocreate.get(key) == value

    key = "r.s"
    prefix = "p.q"
    await ctx_autocreate.set_(key, value, prefix=prefix)
    assert await ctx_autocreate.get(key, prefix=prefix) == value
    assert await ctx_autocreate.get(prefix) == {"r": {"s": value}}
    assert await ctx_autocreate.get(key) is None
