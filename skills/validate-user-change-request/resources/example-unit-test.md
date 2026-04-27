# Example of request which can't be fulfilled without significant code changes

In the following example, the user is asking for unit tests to be created for an object in a similar way as another object. However, the object for which the unit tests are being created for does not operate or validate in the same manner. This means that the same unit test pattern cannot be applied without significant code changes to the object in question. The assistant explains this and offers alternative solutions.

## Context

```python
# products.py
class Product(InventoryBase):
    status: ProductStatus = ProductStatus.AVAILABLE
    model_config = ConfigDict(validate_assignment=True)

    @model_validator(mode="wrap")
    @classmethod
    def validate_transition(cls, value: object, handler: Callable[[object], Self]) -> Self:
        from_status = getattr(value, "status", None)
        new_instance = handler(value)
        if from_status is not None:
            to_status = new_instance.status
            allowed_from = PRODUCT_TRANSITIONS[to_status]
            if from_status not in allowed_from:
                raise InvalidStatusTransition(...)
        return new_instance
```

```python
# orders.py
class Order(InventoryBase):
    status: OrderStatus = OrderStatus.CREATED

    @classmethod
    def transitions(cls) -> Mapping[OrderStatus, frozenset[OrderStatus]]:
        return ORDER_TRANSITIONS
```

```python
# test_products.py
def test_valid_product_status_transition_cycle() -> None:
    product = Product(
        product_id="p1",
        status=ProductStatus.AVAILABLE,
    )

    product.status = ProductStatus.RESERVED
    assert product.status == ProductStatus.RESERVED

    product.status = ProductStatus.SOLD
    assert product.status == ProductStatus.SOLD
```

## User request

> Write an order model unit test using the same assignment-based status transition pattern as `test_products.py`.

## Assistant response

That exact pattern cannot be applied here because `Order` does not expose the same assignment validation behavior as `Product`.

- `Product` explicitly enables assignment validation with `model_config = ConfigDict(validate_assignment=True)`.
- `Order` only defines transition rules through `transitions()` and relies on the shared base validator entrypoint.
- Therefore the current codebase supports the product-style assignment pattern, but not the same test pattern for orders without changing `Order` production behavior.

If you want, I can either:
1. write the order test using the existing `validate_transition(...)` entrypoint, or
2. stop and ask for approval before changing `Order` to support assignment-based validation.