#!/usr/bin/env python3

f = open("/home/pi/.asoundrc", 'w')
f.write(
    """pcm.!default {
    type hw
    card 1
    device 0
}

ctl.!default {
    type hw
    card 1
}
""")
f.close()

print("Default sound card set to 1")
