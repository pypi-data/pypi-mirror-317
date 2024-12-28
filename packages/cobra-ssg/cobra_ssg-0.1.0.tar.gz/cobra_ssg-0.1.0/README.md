# COBRA SSG

This is a static page generator written from scratch with a test driven development (TDD) approach.

## How does it work

```
Note: in the content sections we are about to describe, you have the freedom to create your content files with whatever name you like. That being said, we suggest using names without special characters nor spaces. Camel case or snake case are great for naming folders and files and avoid any complications or weird URLs on your site.
```

A website in Cobra SSG is compose of several elements, all of them contained in the `content` folder. Here are the different elements and how they work:

### Layouts

The `content/layouts` folder contains all the layouts used for the different markdown files when they are converted to html files. There are no subfolders allowed in `content/layouts` except the ones described here.

There are some mandatory files and folders to be found in the `content/layouts` folder:

- `content/layouts/default.html`: this file contains the default layout for your site. It's not used for the blog, as the blog has its own layout files. If a page don't have a layout defined in its front matter in the `layout` variable, this `default.html` file will be used when converting the page's markdown to html.
- `content/layouts/css`: this folder will contain all the css files used on the site.
- `content/layouts/css/global.css`: this file contains all the shared css rules for the site.
- `content/layouts/css/blocks.css`: this file is only mandatory if you have files in the `content/layouts/blocks` folder on the site. If that's not the case, you can skip it. It contains the specific style rules that only the blocks used on the site.
- `content/layouts/blog.html`: this file is only mandatory if you have a `content/blog` folder on the site. If that's not the case, you can skip it. It contains the html layout for the list of posts.
- `content/layouts/css/blog.css`: this file is only mandatory if you have a `content/blog` folder on the site. If that's not the case, you can skip it. It contains the specific style rules that only the post list will use.
- `content/layouts/post.html`: this file is only mandatory if you have a `content/blog` folder on the site. If that's not the case, you can skip it. It contains the html layout for the post details page.
- `content/layouts/css/post.css`: this file is only mandatory if you have a `content/blog` folder on the site. If that's not the case, you can skip it. It contains the specific style rules that only the post content page will use.
- `content/layouts/js/global.js`: this file contains the javascript code shared by the whole site.

In order to create a new layout, you create a file under `content/layouts` with the name of the layout and html extension, like `content/layouts/new-layout.html`. In the content of the file, create the layout in html. Don't include the base tags, like `<html>`, `<head>` or `<body>`, as those will be inserted automatically during the build process.

If you need specific css rules for this new layout, include it in a css file with the same name. In this example, that file would be `content/layouts/css/new-layout.css`.

The layout html content should include a `<cobra_ssg_content>` tag. That tab will be replaced with the content of the actual route. For example, if the page the user is in is `/about` and that page uses de `default` layout, the content of the `content/pages/about.md` page will be inserted in the `<cobra_ssg_content>` place in the html document.

### Blocks

Blocks are chunks of HTML you can place in multiple places in your templates without repeating code. They are located in the `content/layouts/blocks` folder. Their css rules should be placed in the `content/layouts/css/blocks.css` file. The block file should be an html file containing the html of the block. For example, `content/layouts/blocks/main-block.html` could have this content:

```html
<nav>
    <ul>
      <li><a href="/section1">Section 1</a></li>
      <li><a href="/section2">Section 2</a></li>
      <li><a href="/section3">Section 3</a></li>
      <li><a href="/section4">Section 4</a></li>
    </ul>
</nav>
```

To use that you need to put a tag in the desired place inside the html content of the layout with this format: `<block_[name-of-the-block-file]>`. For example, if the block file is `content/layouts/blocks/main-block.html`, then the tag inside the layout using that block should be `<block_main-block>`

### Blog

The `content/blog` folder contains all the articles of the blog. These articles are markdown files with a name in this format: `[YYYY-MM-DD]-name-of-the-article.md`. For example, `2024-09-15-this-is-a-new-blog-post.md`. That makes the files to order from date in a folder setup to order alphabetically. Why don't just use the date of the file instead of the filename? Because the articles can be rewritten, or written later, but with the same published date then before.

The layout used for the list of these files is the one defined in `content/layouts/blog.html`. The layout used for the content view of each file is defined in `content/layouts/post.html`.

The URL of the blog list has the format `https://yoursite.com/blog/1`, where `1` in that example is the number of page in the post list (it's the pagination mechanism). The URL of the posts hang from the `blog` route, like this: `https://yoursite.com/blog/2024-09-15-this-is-a-new-blog-post`.

### Pages

Pages are content that is static and not part of the blog. For example, documentation for a project, or recipes of a specific cuisine style. These are markdown files located in the `content/pages` folder and you can name them as you wish. Subfolders are permitted, and they will be part of the URL structure. For example, if you have a page in `content/pages/spanish-recipes/recipe-1.md`, the resulting URL would be `https://yoursite.com/spanish-recipes/recipe-1`. There is no specific format for naming these pages files and folders.

The layout used for each page should be defined in the markdown front matter with the `layout` variable, like this:

```
---
name: Incredible Page
layout: standard-incredible-layout
---

# Incredible Page

This is the content of the incredible page
```

The value of `layout` in the front matter will be used to look for the proper layout in the `content/layouts` folder, with the `html` extension (in the example, `content/layouts/standard-incredible-layout.html`). If no `layout` variable is found in the front matter, the `content/layouts/default.html` layout will be used at the time of `html` conversion.

## Tests

All the tests in Cobra SSG are placed in `test_cobra_ssg_e2e.py`. As the file implies, they are end to end tests, testing the whole logic at the same time.

In order to execute it, run the `test.sh` file in your terminal. Before that you need to install the dependencies with `poetry install` on the root of the project.