# tengen
Generate string using template

## Concept
Use templates to simplify string replacement

**[done.tngn]**
```
{0} is done.
```

## What is possible
1. String replacement using templates

## Reason for development
- I want to make string replacement easier using templates

## Versions

|Version|Summary|
|:--|:--|
|0.1.6|Release tengen|

## Installation
### tengen
`pip install tengen`

## CLI
### render
Rendering using templates

#### 1. Prepare template file(done.tngn)
**[done.tngn]**
```
{0} is done.
```

#### 2. Rendering templates by CLI execution

```
render # <template name> <args>
  [With value]
    -o|--output  # Output file path
```
`tengen render done TENGEN`
```
TENGEN is done.
```
