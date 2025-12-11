# Understanding preloaded objects

**Revision:** 2  
**Language:** en


For each incoming request njs creates a separate virtual machine.
This brings a lot of benefits such as predictable memory consumption
or requests isolation.
However, as all requests are isolated,
if a request handler needs to access some data,
it has to read it by itself.
This is not efficient especially when the amount of data is large.

To address this limitation,
a preloaded shared object was introduced.
Such objects are created immutable and do not have prototype chains:
their values cannot be changed, properties cannot be added or removed.

## Working with preload objects {#working_with_preload_objects}

Here are some examples of how to work with a preload object in njs:


- access properties by name:

```
preloaded_object.prop_name
preloaded_object[prop_name]
```
- enumerate properties:

```
for (i in preloaded_object_name) {
    ...
}
```
- apply non-modifying built-in methods using `call()`:

```
Array.prototype.filter.call(preloaded_object_name, ...)
```
