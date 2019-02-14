


import alsaaudio

cards = alsaaudio.cards()
mixers = alsaaudio.mixers()

mixers = alsaaudio.mixers(1) # Get access to card at position number 2 (0, 1...)
mix = alsaaudio.Mixer(control="Master", cardindex=1)
mix.getvolume()
mix.setvolume(50)
mix.getrange()
mix.setvolume(50*87/100)

# Control "Master", "Speaker", "PCM", "Headphone"... Which one?

#mixer = alsaaudio.Mixer(control="Master")
#alsaaudio.Mixer(control=mixers[1])

headphone = alsaaudio.Mixer(control="Headphone")
pcm = alsaaudio.Mixer(control="PCM")


#mixer.setvolume(50)
initvolume = mixer.getvolume()
initvolume = initvolume[0]

mixer.setvolume(100)
headphone.setvolume(100)
pcm.setvolume(100)

volume1 = mixer.getvolume()

mixer.setvolume(initvolume)
finalvolume = mixer.getvolume()
finalvolume = finalvolume[0]

print volume1, finalvolume
