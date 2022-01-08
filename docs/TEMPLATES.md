# Thymine Templates

## The Basics
Templates give users full control over how their website looks and feels, allowing for extensibility and customization.

Here's some HTML5 boilerplate:
```html
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

## Styling
Every website that looks decent has CSS. We can use CSS to style our generated HTML.

`hello.template.css`
```css
.thymine-container {
  margin: 2rem 2rem;
}
.thymine-container h1 {
  color: red;
}
```

Let's add our CSS styling to our HTML template with `<link rel="stylesheet" href="hello.template.css">`
`hello.template.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>$THYMINE_META.TITLE</title>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <link rel="stylesheet" href="hello.template.css">
</head>
<body>
  <div class="thymine-container">
    $THYMINE_BODY
  </div>
</body>
</html>
```

Finally, we can tell Thymine to move our css file into the build folder by supplying its path as a string under `extras` in our template configuration.

`templates.json`
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
    "main_template": "path/to/hello.template.html",
    "extras": [
      "path/to/hello.template.css"
    ]
  }
}
```

NOTE: In larger projects where the same template is repeatedly used, this is not ideal. You might want to have a project structure like
```
./
├─styles/
  ├─ hello.template.css
├─pages/
  ├─ page1.html
```
and change the `href` to something like `/styles/hello.template.css`, while serving from the root of the project.

Let's recompile with `python3 main.py hello.tym build/ -t Hello_Template` again.

![hello.html in browser](https://raw.githubusercontent.com/t0a5ted/thymine/master/docs/assets/template-out-1.png)