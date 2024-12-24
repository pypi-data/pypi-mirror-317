# Tutorial: Setup Email Access

!!! note "Only for Google Mail"

    This tutorial demonstrates how to set up programmatic email access
    using [App Passwords](https://support.google.com/accounts/answer/185833?hl=en). Note that
    nothing in this tutorial is specific to `sxolar` and can be used with any Python library that
    requires email access. We include this tutorial here because `sxolar` can send email summaries
    of search results.

## Option 1 (For MFA): Create an App Password

Note that this step is only applicable to accounts that have mutli-factor authentication enabled.
If you do not have multi-factor authentication enabled, you can skip this step.

1. Go to [App Passwords](https://myaccount.google.com/apppasswords).
2. Enter an app name, e.g. "SampleApp".
3. Click "Create".
4. Copy the generated app password.

The generated app password is a 16-character code that you will use to authenticate your application.

```plaintext
App password: "abcd efgh ijkl mnop"
```

## Option 2 (No MFA): Enable Less Secure Apps

If you do not have multi-factor authentication enabled, you can enable access for less secure apps.

1. Go to [Less Secure Apps](https://myaccount.google.com/lesssecureapps) and turn on access for less secure apps.
2. Go to [Display Unlock Captcha](https://accounts.google.com/DisplayUnlockCaptcha) and click continue.
3. Go to [App Passwords](https://myaccount.google.com/apppasswords) and create a new app password.


!!! note "Future Deprecation Possible"

    Google has announced that they will be [disabling less secure apps](https://support.google.com/accounts/answer/6010255?hl=en)
    in the future. It is also possible that they may deprecate App Passwords in the future. We recommend using the
    App Password method if you have multi-factor authentication enabled.


## Using with `sxolar`

The generated app password can be used with `sxolar` to send email summaries of search results. You can specify the
app password either as a command-line argument or as an environment variable.

### Command-Line Argument

When using the `sxolar summary` command, you can specify the app password using the `--email-password` option.

```bash
sxolar summary ... --gmail-app-password "abcd efgh ijkl mnop"
```

### Environment Variable

You can also set the app password as an environment variable. The `sxolar` package checks
for the specific environment variable `SXOLAR_EMAIL_APP_PASSWORD` to get the app password.

```bash
export SXOLAR_EMAIL_APP_PASSWORD="abcd efgh ijkl mnop"
```

Then you can use the `sxolar summary` command without specifying the app password.

```bash 
sxolar summary ...
```
