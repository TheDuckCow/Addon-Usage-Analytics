# Addon-Usage-Analytics
This addon for blender shows a mostly stripped down example for how to add analytic usage tracking to your blender addons.

## What this addon does

- Users can opt in or out of analytics tracking
- When operators defined by the addon are used, the timestamp, version, and name are pushed to the database server
- Built-in auto detection for available updates

While this addon uses parse as the easy, free (for low user base) solution for database storage, there are plenty of alternative methods and third parties services that could be use. I find this to be the simplest to implement, but other solutions may be out there. A potential extension of this would also be direct connection to a google analytics account, a useful analytics platform. This most likely can be accomplished by setting up "events" in GA and triggering the requests from python's http library.

## Steps to implement your own
1. Create a parse app (parse.com)
2. Save the app key and rest api key to the according variables below (note security point)
3. Create the classes "usage" and "usage_dev" on parse (under the data tab)
4. Put the function call >> usageStat(function) << at the beginning of each operator's execution function
5. *Set v (verbose) to false before distributing the addon!*

## Parse setup
Coming soon.

## Warnings and considerations
*With great power comes great responsibility.* Use this code wisely, and don't do anything malicious. This addon demo is setup so that analytics are only captured if the user explicitly opts into tracking, and the information pushed is entirely anonymous. Python of course is unlimited, and you can of course build upon the functionality and extent of what you capture through the analytics. You should always be very transparent with your users what information is being tracked, and avoid taking traceable, personal information. 

For instance, in my own use of these analytics, I built a system to also include how many times a single user has used a specific function as well as when the user installed the addon in the first place - but I made sure this information was still anonymous and didn't browse through the user's filesystem outside addon's self-contained directory.

## Security concerns
Integration with parse via python is clean and easy, but be careful. Anyone who knows your app and api keys can potentially start controlling your core data, adding, changing, or deleting information. The keys included in the code are easily visibly to anyone who looks at the script unless you add in extra precautions. 

For example, in my own addons where I use this kind of analytics tracking, I don't have the keys hard included in the addon but rather pull it from another server. This is a little more complex, but is certainly safer depending on how it's done.

## Free to use, free to modify, not free to blame me :)
I'm attaching this code with the MIT license. That means it's "as-is", and is without any warranty. If things don't work or you overstep privacy boundaries through modifications of this addon, I am not held liable. 
