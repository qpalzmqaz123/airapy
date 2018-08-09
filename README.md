# AIRA

Aira is a simple script language based on python3, it intend to learn how to make a script language.

## Installation

```bash
$ git clone https://github.com/qpalzmqaz123/aira.git

$ cd aira

$ python3 setup.py install
```

## Usage

```bash
Usage: aira [OPTIONS] FILE

Options:
  --debug  Show debug info.
  --help   Show this message and exit.
```

## Examples

### hello world

```ruby
print('hello world')
```

### Variable

```ruby
a = 1
a = b = '123'
```

### Function

```ruby
sum = fn(x, y) do
    return x + y
end

print(sum(2, 3))
```

### Branch

```ruby
a = 1

if a >= 1 do
    print('a >= 1')
else
    print('a < 1')
end
```

### Loop

```ruby
i = 0
while i < 5 do
    print(i)

    i += 1
end
```

### Exception

```ruby
a = 0

try do
    a = 1
    throw Error()
catch err do
    a = 2
end

print(a)
```

### Array & Hash

```ruby
a = [1, 2, 3]
a.insert(0, 0)
a.pop()
print(a)

b = {'a': 1}
b.b = 2
print(b)
```

### Closure

```ruby
get_counter = fn() do
    cnt = 0

    return fn() do
       return @cnt += 1
    end
end

counter = get_counter()

print(counter())
print(counter())
print(counter())
print(counter())
print(counter())
```

### Fibonacci sequence

```ruby
n = 10

res = []

sum = fn(index) do
    if index <= 0 do
        throw Error('index must be greater than 0')
    end

    if index == 1 or index == 2 do
        return 1
    end

    return sum(index - 1) + sum(index - 2)
end

i = 1
while i < n + 1 do
    res.push(sum(i))

    i += 1
end

print(res)
```
