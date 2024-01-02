# notes to self
bot process
main
* capture
* distinguish beg from actual post
* post to discord

healthcheck process (separate process?)
health determined by most recent msg (captured by bot? or sent to discord?)
could be both

* check if MS down (via taskman? unsure)
* check if bot down 
    (healthcheck: when did it write a txt msg)
* check if discord integration down (bot alive, can't post)
    (healthcheck: when was the bot's last msg in the discord channel)
    
## TODO list
* ~~fix the invite link to be not hardcoded.~~
* ~~fix deleting messages (get channel from context instead of reusing context)~~
* get the thing to send image/screenshots
* blocklist certain symbols (registered logo ®, degree, pipe |, ™, ©)
* create a better pip installation txt file... thing.
* optional location checks (shrine, leafre, henesys, odium?)
* healthcheck stuff listed above