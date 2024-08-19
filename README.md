# How-to

This site is built using [Hugo](https://gohugo.io/installation/) and [bear-cub theme](https://github.com/clente/hugo-bearcub)

There's a Workflow that will publish any modification you make to the repo to Github Pages. The workflow is in `.github/workflow/hugo.yaml`

You can test the site locally following the information on the Hugo site and cloning this repo locally. 

## Images
All images should be store in the `static` directory and can then be access directly from the root `/` when the site is published.  
There's a small difference in how GitHub Pages and the local version will render/access the images.

## Pages
All pages are in the `content` folder. If you add a new file, it will add that page to the menu. Make sure to change the `weight` to the position where you want you menu to appear. 
If you want to add content to an existing page you can easily do that directly within GitHub. Just modify the right `.md` file.  
**NB**: Never make any changes to the `public` folder. This directory is over written every time the site is modfied.

## URL
This site can be viewed by visiting https://snowcon-info.github.io/ or https://snowcon.info
