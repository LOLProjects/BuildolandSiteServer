# BuildolandSiteServer
The server code that will handle the server and all


## Emails
Of course I'm gonna have to cut corners with emails, otherwise I wouldn't be finishing this site. Here are some notable things about how an email **should** work and how mine works:

- test@mailbox.com is different from test@MAILBOX.com, but TEST@mailbox.com is the same as test@mailbox.com, not here mate.
- ALL emails will be read as their lowercase equivalents. So GMAIL will be read as gmail, sorry GMAIL.
- The `+` icon in one such as test+bdl@mailbox.com should be supported and treated the same as test@mailbox.com. I've not been able to test it yet since we've not openned an account for bdl
- The outerlevle domain (.com or .org) can only be in 2-4 length. So no test@mailbox.hello, only hell is allowed (No they won't be cut short, it will return an error, that was just a joke)
- I am allowing emails such as yoyo.daug_mate+bdl@mailbox.com. That's about as far as support goes.
- No, there won't be any `yoyo\@getFooled.idiot@mailbox.com` or `yoyo";';'214ad@@@"@mailbox.com`. Not even sublime recognizes that as email in its syntax highliting, which means I shouldn't.
And I think that's it. Not that bad afterall

## TODO (11)
1. bdl/auth.py:12       Add change password
2. bdl/auth.py:14       Finish login
3. bdl/auth.py:19       Refactor register
5. bdl/auth.py:67       Send a verification email
6. bdl/auth.py:98       Finish forgot pass
7. bdl/cli.py:6         Add user, list users, and remove user
8. bdl/cli.py:14        add-code should accept variadic arguments
9. bdl/main.py:6        Get user_id from session before each request
10. bdl/main.py:7       Allow username change
11. auth/login.html:4   Login -- Add flashes

