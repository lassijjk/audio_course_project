# audio_course_project
Project done as part of Audio Processing course at Tampere University.  

Topic was separation of harmonic and percussive elements according to paper 
SEPARATION OF A MONAURAL AUDIO SIGNAL INTO HARMONIC/PERCUSSIVE COMPONENTS BY COMPLEMENTARY DIFFUSION ON SPECTROGRAM.
Ono, N., Miyamoto, K., Le Roux, J., Kameoka, H., & Sagayama, S. (2008, August).

So the goal was to create a program, which would separate drums from an audio track. The best
performance was evaluated with k = 20, alpha = 0.3 and gamma = 0.3.

Biggest challenges was getting started with the algorithm,
and once it was done it needed a bit of optimization with initial runs of 6 minute song
taking 15 minutes. I managed to reduce it to 1/100 of the initial length, to a whopping 9 seconds. 
