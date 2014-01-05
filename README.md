Tanks (Work in progress)
=====

Worms like artillery game, written in python with pygame.

Features:
	Destructible terrain
	Procedurally generated terrain
	Projectile physics
	Multiple player types
	Animated sprites

TODO:
	The current layer/rendering system is way too slow! I've seen other pygame games running much better fps using blit and colorkey based transparency on images. I originally had some problems with that approach, but doing things pixel by pixel in python is just too slow.

	Establish a win condition.

	Turn changes should be more obvious, and the turn time limit should be displayed.

	Players should be able to choose their character.

	Title screen and menu/UI in general

	Characters should take damage when caught in a bullet's blast radius.

	Tank animations.

	More characters and projectiles.

	Characters move faster when going uphill and can easily become airborne when going downhill. This is an undesirable side effect of the current implementation and looks kind of weird.

	Online multiplayer support.

	More background and terrain images.
