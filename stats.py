"""
This sample code is being released without any license or warranty.
Use at your own risk, and be mindful to make sure users know what
data is being shared, if it is being shared, and provide the option
to opt-out if it isn't already an opt-in situation.

This demo addon only records what function users use and the time
when they use it. It does not capture any geo data and no piece of
data is traceable back to a specific user.

For more information, go to:
https://github.com/TheDuckCow/Addon-Usage-Analytics

"""

bl_info = {
	"name": "Demo Usage Analytics",
	"category": "Object",
	"version": (1, 0, 1),
	"blender": (2, 74, 0),
	"location": "3D window toolshelf > Tools tab",
	"description": "Demo addon for capturing anonymous user data for analytics",
	"warning": "",
	"wiki_url": "https://github.com/TheDuckCow/MCprep",
	"author": "Patrick W. Crawford <support@theduckcow.com>"
}


import bpy
v = True # verbose, for debugging. Will also push data up to a _dev parse class instead of publicly used class
ver = '(1, 0, 1)' # for pushing the version up to the database, useful to know

# app keys, specific to each Parse app. Be careful with the security of this!
appkey = ""  #"the App key" 
restkey = ""  #"the REST API key"
classname = 'usage'


def usageStat(function):
	addon_prefs = bpy.context.user_preferences.addons[__name__].preferences
	
	# if the user hasn't opted in, don't send the stats
	if not addon_prefs.stats_optin:
		return
	
	# otherwise, send the thing!
	#if v:print("version? ",__version__)
	vr = ver
	if v:vr+=' dev' #extra debugging, so you can separate testing data versus real user data
	if v:print("Running usageStat for: {x}".format(x=function))
	
	# always enclose in try - if something goes wrong, shouldn't prevent user from using function
	# remove try statement for developing purposes
	try:
		import urllib.request
		import json,http.client
		ak = appkey
		rk = restkey
		connection = http.client.HTTPSConnection('api.parse.com', 443)
		connection.connect()
		d = ''
		if v:d="_dev"
		connection.request('POST', '/1/classes/'+classname+d, json.dumps({
			   "function": function,
			   "version":vr,
			 }), {
				"X-Parse-Application-Id": ak,
				"X-Parse-REST-API-Key": rk,
				"Content-Type": "application/json"
			 })
		result = json.loads(  (connection.getresponse().read()).decode()  )
		if v:print("Sent usage stat, returned: {x}".format(x=result))
	except:
		if v:print("Failed to send stat")
		return


def checkForUpdate():
	addon_prefs = bpy.context.user_preferences.addons[__name__].preferences
	try:
		if addon_prefs.checked_update:
			return addon_prefs.update_avaialble
		else:
			# the code below will run at most once per blender session
			addon_prefs.checked_update = True
			import urllib.request
			# obviously change this website to the according one and change the parsing to fit
			page = urllib.request.urlopen("https://raw.githubusercontent.com/TheDuckCow/Addon-Usage-Analytics/master/stats.py",timeout=10).read().decode('utf-8')
			
			# parse for the version ID parsed from whatever website, will depend on the context/setup
			tmp = page.split('"version": ')[1]
			currentVersion = tmp.split(')')[0]+')'
			
			# check to see if the versions match, assumes if they are different it means local is outdated
			if currentVersion != ver:
				if v:print("Addon is outdated")
				# create the text file etc.
				addon_prefs.update_avaialble = True
				return True
			else:
				if v:print("Addon is not outdated")
				addon_prefs.update_avaialble = False
				return False
	except:
		pass


########
# Sample operator setup that will be usage tracked
class OBJECT_OT_add_object(bpy.types.Operator):
	"""Create a new Mesh Object"""
	bl_idname = "mesh.add_object"
	bl_label = "Add Mesh Object"
	bl_options = {'REGISTER', 'UNDO'}


	def execute(self, context):
		#run the stats function
		if v:print("Running the add object function, first stats...")
		usageStat("Add Object")
		if v:print(".. and now to add to object ..")
		# do whatever the function would do, in this case add a cube
		bpy.ops.mesh.primitive_cube_add()
		return {'FINISHED'}


########
# quickly open release webpage for update
class openreleasepage(bpy.types.Operator):
	"""Open the webpage to get the latest version of this addon"""
	bl_idname = "object.openreleasepage"
	bl_label = "Open the addon release page"

	def execute(self, context):
		try:
			import webbrowser
			webbrowser.open("https://github.com/TheDuckCow/Addon-Usage-Analytics")
		except:
			pass
		return {'FINISHED'}


#######
# Demo panel to showcase stats tracking
class demoPanel(bpy.types.Panel):
	"""Demo panel for showing stats tracking"""
	bl_label = "Demo Stats Panel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = 'Tools'

	def draw(self, context):
		
		layout = self.layout
		split = layout.split()
		col = split.column(align=True)
		#col.label(text="is it working")
		split = layout.split()
		col = split.column(align=True)
		col.operator("mesh.add_object", text="Add Object")
		split = layout.split()
		col = split.column(align=True)

		# section for showing update if one is available
		# to test this, change the version number above
		if checkForUpdate():
			col.label (text="Update available!", icon='ERROR')
			split = layout.split()
			col = split.row(align=True)
			col.operator("object.openreleasepage", text="Get it now")


#######
# preferences UI
class userPreferencesPanel(bpy.types.AddonPreferences):
	bl_idname = __name__

	stats_optin = bpy.props.BoolProperty(
		name = "stats_optin",
		description = "If enabled, anonymous data about how these addon functions are used will be sent to the developers for continued support",
		default = False)
	checked_update = bpy.props.BoolProperty(
		name = "checked_update",
		description = "Check once and once only for an update",
		default = False)
	update_avaialble = bpy.props.BoolProperty(
		name = "update_avaialble",
		description = "True if an update is available",
		default = False)

	def draw(self, context):
		layout = self.layout
		row = layout.row()
		row.label(text="Consider opting into analytics to help future development!")
		col = layout.row(align=True)
		if self.stats_optin:
			col.prop(self, "stats_optin", text="Press to opt OUT of anonymous usage tracking", icon='CANCEL')
			col = layout.row(align=True)
			col.label(text="Be sure to save user preference to keep the optin enabled!")
		else:
			col.prop(self, "stats_optin", text="Press to opt into of anonymous usage tracking", icon='HAND')


def register():
	bpy.utils.register_class(userPreferencesPanel)
	bpy.utils.register_class(OBJECT_OT_add_object)
	bpy.utils.register_class(openreleasepage)
	bpy.utils.register_class(demoPanel)
	

def unregister():
	bpy.utils.unregister_class(userPreferencesPanel)
	bpy.utils.unregister_class(openreleasepage)
	bpy.utils.unregister_class(demoPanel)
	bpy.utils.unregister_class(OBJECT_OT_add_object)

if __name__ == "__main__":
	register()
