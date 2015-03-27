# Kadabra

Kadabra v1.1_beta: Automatic LFI Exploiter and Scanner

Author: D35m0nd142, <d35m0nd142@gmail.com>

Follow me on: https://twitter.com/d35m0nd142

Tutorial Video: https://www.youtube.com/watch?v=iE1ILC86fYk

To report any kind of problem mail me to the email address written above.

This is a beta release, in fact the project is almost complete but there is still one way of attack to implement. It is the /proc/self/fd attack and I am working on it. As soon as possible I will publish the updated version of Kadabra but for the moment use it as is or don't use it ;) 

The /proc/self/environ attack should work fine with all the http header parameters I put in the code (LOOK AT THEM at least once) but if I had to advise you to choose one of them, I would suggest you to use the classic parameter User-Agent.
Remember that you have to put in the parameter in the way it has showed in the vulnerable page (example: User-Agent must be written (usually) USER_AGENT or HTTP_USER_AGENT) because Kadabra will look for it within the output file and if it does not find the proper "string" it will not work clearly.

Compile the software using "bash make.bash" if you want to be sure it will work and MAKE SURE TO USE THE SOFTWARE PROPERLY.

I do not take any responsability for the use you are going to make of this software. This was created for not malicious purposes and keep in mind that if you will perform any crime, voluntarily or not, you will be the only one responsible for that. 

D35m0nd142
