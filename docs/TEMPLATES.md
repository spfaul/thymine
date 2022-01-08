# Thymine Templates

## Getting Started
Templates give users full control over how their website looks and feels, allowing for extensibility and customization.

Here's some HTML5 boilerplate:
```
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Hello, world!</title>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <meta name="description" content="" />
</head>
<body>
</body>
</html>
```

Now, here's what a boilerplate thymine template would look like: 

`hello.template.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Hello, world!</title>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
</head>
<body>
	<div class="thymine-container">
		$THYMINE_BODY
	</div>
</body>
</html>
```

Thymine replaces all instances of `$THYMINE_BODY` in the source file with the generated HTML body of your transpiled `.tym` file.

Simple enough?

You can also access metadata of the `.tym` source file with `$THYMINE_META.<key>`.
With this information, we can make a few edits to our template.

`hello.template.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>$THYMINE_META.TITLE</title>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
</head>
<body>
  <div class="thymine-container">
    $THYMINE_BODY
  </div>
</body>
</html>
```

Now, the title of the webpage in the browser changes to the value specified under `TITLE` in the source's metadata.

