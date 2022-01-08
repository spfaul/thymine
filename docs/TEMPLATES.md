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

Let's create a `.tym` file to test our template.

`hello.tym`
```
-
TITLE: My Blog!
-
# Hello, World!
```

Almost Done! Finally, we need to tell Thymine about our template files. To do that, edit `templates.json` in Thymine's root directory as follows:

```json
{
  // This template is for debugging/development purposes, ignore it.
  "debug": {
      "main_template": "examples/test.template.html",
      "extras": [
            "examples/test.template.css"
      ]
  }

  // Here we add our new template
  "Hello_Template": {
    "main_template": "path/to/hello.template.html"
  }
}
```

All set! To compile on Linux/MacOS, run `python3 main.py hello.tym build/ -t Hello_Template`.

We can view our final generated HTML file at `build/hello.html`.

![hello.html in browser](https://raw.githubusercontent.com/t0a5ted/thymine/master/docs/assets/template-out-0.png)