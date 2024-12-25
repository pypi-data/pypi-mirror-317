# Django CMS SEO Extension

## Overview

The Django CMS SEO Extension is a simple, flexible, and easy-to-use tool for managing SEO-related meta tags directly from the Django CMS admin interface. This extension provides support for basic meta tags, Open Graph tags, and Twitter Card tags, making it easy to enhance the visibility and social media integration of your website.

## Features

-   **Meta Tags**: Define standard meta tags such as keywords, description, author, etc.
-   **Open Graph Meta**: Add Open Graph tags for better integration with social platforms like Facebook.
-   **Twitter Card Meta**: Manage Twitter Card tags to enhance how your content appears on Twitter.
-   **Admin Integration**: Manage all tags directly from the Django admin interface with inlines and filters.
-   **SEO HTML Generation**: Generate the SEO meta tags dynamically for each page.

## Installation

1. **Install the package:**

    You can add the package to your project by running:

    ```bash
    pip install djangocms-seo
    ```

2. **Add to `INSTALLED_APPS`:**

    Add the extension to your Django settings:

    ```python
    INSTALLED_APPS = [
         ...,
         'cms',
         'menus',
         'treebeard',
         'sekizai',
         'djangocms_text_ckeditor',
         'djangocms_seo',
    ]
    ```

3. **Apply Migrations:**

    Run the following commands to apply the necessary migrations:

    ```bash
    python manage.py migrate
    ```
    Sometimes this will throw an error like ```no table "cms.page"```, if that happens you can just comment  ```'djangocms_seo'``` from your ```INSTALLED_APPS``` and migrate normally to create the necessary ```djangocms``` tables, then uncomment ```'djangocms_seo'``` and run :
    ```bash
    python manage.py migrate djangocms_seo
    ```
    It should work without issues.  
    
    ---

## Usage

1. **Create Meta Tags:**

    From the Django CMS admin interface or directly from the CMS toolbar, navigate to the `Meta Tags`, `Open Graph Meta`, or `Twitter Card Meta` sections and create the necessary tags.

2. **Integrating in your template:**

    Use the `seo_meta_tags` template tag in your base template to generate the meta tags dynamically:

    ```html+django
    <!DOCTYPE html>
    {% load seo_tags %}
    <html lang="en">
         <head>
              <meta charset="utf-8" />
              ...
              {% seo_meta_tags %}
    ```

3. **Assign Meta Tags to a Page:**

    Edit a page in the CMS. Under the "Advanced Settings" tab, you will find the fields to add SEO tags. You can select from existing tags or create new ones on the fly.

4. **Extend SEO Functionality:**

    You can extend the models or admin interface as needed. See the documentation for more details.

## Models

-   **MetaTag**: Stores standard meta tags with name and content.
-   **OpenGraphMeta**: Stores Open Graph meta tags with property and content.
-   **TwitterCardMeta**: Stores Twitter Card meta tags with name and content.
-   **SeoExtension**: Associates meta tags with CMS pages.

## Admin

-   **MetaTagAdmin**: Admin interface for managing Meta Tags.
-   **OpenGraphMetaAdmin**: Admin interface for managing Open Graph tags.
-   **TwitterCardMetaAdmin**: Admin interface for managing Twitter Card tags.
-   **SeoExtensionAdmin**: Admin interface for associating tags with CMS pages.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find a bug or have a suggestion.

## License

This project is licensed under the BSD License. See the `LICENSE` file for details.
