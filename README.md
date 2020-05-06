# BuildolandSiteServer
The server code that will handle the server and all

## Emails
Of course I'm gonna have to cut corners with emails, otherwise I wouldn't be finishing this site. Here are some notable things about how an email **should** work and how mine works:
- test@mailbox.com is the same as test@MAILBOX.com, but TEST@mailbox.com is different from test@mailbox.com, not here mate. (FOR NOW)
- ALL emails will be read as their lowercase equivalents. So GMAIL will be read as gmail, sorry GMAIL.
- The `+` icon in one such as test+bdl@mailbox.com should be supported and treated the same as test@mailbox.com. I've not been able to test it yet since we've not opened an account for bdl
- The outerlevle domain (.com or .org) can only be in 2-4 length. So no test@mailbox.hello, only hell is allowed (No they won't be cut short, it will return an error, that was just a joke)
- I am allowing emails such as yoyo.daug_mate+bdl@mailbox.com. That's about as far as support goes.
- No, there won't be any `yoyo\@getFooled.idiot@mailbox.com` or `yoyo";';'214ad@@@"@mailbox.com`. Not even sublime recognizes that as email in its syntax highliting, which means I shouldn't.
And I think that's it. Not that bad afterall

## Why?
I believe it's good to document why certain design choices were made, so that we can later refer to them when we are in doubt. Choices like requiring accounts, requiring verification, and so on. So why do we have those?

### Accounts
Accounts on the site mainly exist for one very important reason. The game is not going to be free. Having an account allows players to redownload the game without repurchasing it. Ok, but what do we need verification for?

### Verification

Verification exists for two reasons. One, it disallows a player to use an email that's not his, removing the ability to block others from making their own accounts. It also exists to ensure that the email is valid, since there's no other reliable way to check. If the email was invalid but registered, it could be changed by the user before it becomes a problem. As a bonus it also ensures that the game is being bought by a human instead of a bot, however, if a bot is interested in giving a few bucks, please email me at amrojjeh@gmail.com.

### Cookies
I needn't explain why I must eat cookies, but I must explain why I use them for the site. They are used to store the user_id, so that the user doesn't have to login on every request. It might be worthwhile to spend time modifying the value just to test security.

## Verification
Here's how verificaiton is done:
1. User makes an account, server sends an email
2. User clicks on the link provided by the email, which should look like: www.buildoland.com/verify/id=125125215871248
3. If user is logged in, and the id is the same as the logged in user, then that would be verified, otherwise nothing changes

## Config
There are a couple of important variables to note of. Here they are:
- EMAIL: It is the email that is going to be used to send the verification email and other update emails. (ex: "example@gmail.com")
- EMAIL_PASS: The password to the email.
- SMTP: The SMTP server that's going to be used. (ex. smtp.gmail.com)
- DNS: The base url for hosting the site. (ex. "http://localhost:5000/")
- SECRET_KEY: The SECRET_KEY that will be used to encrypt cookies
- DATABASE: The location of the database
