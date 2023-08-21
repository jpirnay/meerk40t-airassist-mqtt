def module_plugin(module, lifecycle):
    """
    This plugin attaches to the module/wxMeerK40t for the opening and closing of the gui. If the gui is never
    launched this plugin is never activated. wxMeerK40t is the gui wx.App object. If the module is loaded several times
    each module will call this function with the specific `module`

    :param module: Specific module this lifecycle event is for.
    :param lifecycle: lifecycle event being regarded.
    :return:
    """
    # print(f"module:airassist {lifecycle}")
    if lifecycle == "module":
        # Responding to "module" makes this a module plugin for the specific module replied.
        return "module/wxMeerK40t"
    elif lifecycle == "module_open":
        # This is relevant the GUI has launched and we want to add some stuff to it
        # print("wxMeerK40t App was lauched.")
        # print("Properties of module:")
        # print(vars(module))
        has_mqtt_module = False
        try:
            import paho.mqtt

            has_mqtt_module = True
        except ModuleNotFoundError:
            pass


        if has_mqtt_module:
            register_gui_stuff(module)

        # The interface for adhoc updating in code

    elif lifecycle == "module_close":
        # print("wxMeerK40t App was closed.")
        # Nothing particular needs to be done here so we just ignore it...
        pass
    elif lifecycle == "shutdown":
        # print("wxMeerK40t App shutdown.")
        # Nothing particular needs to be done here so we just ignore it...
        pass


def coolant_plugin(kernel, lifecycle):
    """
    Barcode plugin. Catches the lifecycle it needs registers some values.

    @param kernel:
    @param lifecycle:
    @return:
    """
    if lifecycle == "register":
        has_mqtt_module = False
        try:
            import paho.mqtt

            has_mqtt_module = True
        except ModuleNotFoundError:
            pass

        if has_mqtt_module:
            try:
                coolant = kernel.root.coolant
            except AttributeError:
                print ("This version of MeerK40t does not have coolant suport")
                return

            register_coolant_support(kernel)


def plugin(kernel, lifecycle):
    """
    This is our main plugin. It provides examples of every lifecycle event and what they do and are used for. Many of
    these events are simply to make sure some module events occur after or before other module events. The lifecycles
    also permit listeners to attach and detach during the lifecycle of a module, and insures everything can interact
    smoothly.

    :param kernel:
    :param lifecycle:
    :return:
    """
    # print(f"Kernel plugin calling lifecycle: {lifecycle}")
    if lifecycle == "plugins":
        """
        All plugins including ones added with this call are added to the kernel. A list of additions plugins will add
        those to the list of plugins.
        """
        return [module_plugin, coolant_plugin]
    if lifecycle == "service":
        """
        Responding to this with a service provider makes this plugin a service plugin.

        Note: Normally we ignore this lifecycle.
        """
        return None  # This is not a service plugin, check service_plugin for an example of that.
    if lifecycle == "module":
        """
        Responding to a registered module provider makes this plugin a module plugin.

        Note: Normally we ignore this lifecycle.
        """
        return None  # This is not a module plugin, check module_plugin for an example of this.
    if lifecycle == "precli":
        """
        This lifecycle occurs before the command line options are processed. Anything part of the main CLI is processed
        after this.
        """
    if lifecycle == "cli":
        """
        This life cycle is intended to process command line information. It is sometimes used to register features or
        other flags that could be used during the invalidate.
        """
        if kernel.lookup("invalidating_plugin_existed"):
            print("Our invalidating plugin existed and put this here.")
    if lifecycle == "invalidate":
        """
        Invalidate is called with a "True" response if this plugin isn't valid or cannot otherwise execute. This is
        often useful if a plugin is only valid for a particular OS. For example `winsleep` serve no purpose for other
        operating systems, so it invalidates itself.
        """
        # Let's test for the existence of our two main components:
        has_mqtt_module = False
        try:
            import paho.mqtt

            has_mqtt_module = True
        except ModuleNotFoundError:
            pass

        if has_mqtt_module:
            return False  # We are valid.
        else:
            return True  # We are lacking central components

    if lifecycle == "preregister":
        """
        During the pre-register phase the module wxMeerK40t is registered and opened in gui mode.
        """
        pass
    if lifecycle == "register":
        """
        Register our various processes. These should modify the registered values within meerk40t. This stage is
        used for general purpose lookup registrations.
        """
        # See simple plugin for examples of registered objects.
        pass

    if lifecycle == "configure":
        """
        Configure is a preboot stage where everything is registered but elements are not yet booted.
        """
        pass
    elif lifecycle == "boot":
        """
        Start all services.

        The kernel strictly registers the lookup_listeners and signal_listeners during this stage. This permits modules
        and services to listen for signals and lookup changes during the active phases of their lifecycles.
        """
        pass
    elif lifecycle == "postboot":
        """
        Registers some additional choices such as some general preferences.
        """
    elif lifecycle == "prestart":
        """
        CLI specified input file is loading during the pre-start phase.
        """
        pass
    elif lifecycle == "start":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "poststart":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "ready":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "finished":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "premain":
        """
        Nothing happens.
        """
        pass
    elif lifecycle == "mainloop":
        """
        This is the start of the gui and will capture the default thread as gui thread. If we are writing a new gui
        system and we need this thread to do our work. It should be captured here. This is the main work of the program.

        You cannot ensure that more than one plugin can catch the mainloop. Capture of the mainloop happens for the
        duration of the gui app, if one exists.
        """
        pass
    elif lifecycle == "postmain":
        """
        Everything that was to grab the mainloop thread has finished. We are fully booted. However in most cases since
        the gui has been killed, the kernel has likely been told to shutdown too and will end shortly.
        """
        pass
    elif lifecycle == "preshutdown":
        """
        Preshutdown saves the current activated device to the kernel.root to ensure it has the correct last value.
        """
        pass

    elif lifecycle == "shutdown":
        """
        Meerk40t's closing down. Our plugin should adjust accordingly. All registered meerk40t processes will be stopped
        any plugin processes should also be stopped so the program can close correctly. Depending on the order of
        operations some operations might not be possible at this stage since the kernel will be in a partially shutdown
        stage.
        """
        pass


def register_coolant_support(kernel):
    from .mqtt_logic import AirAssist

    _ = kernel.translation
    print ("Register coolant")

def register_gui_stuff(module):
    import wx

    from .gui import ConfigDialog

    print ("Register GUI")

    context = module.context
    kernel = context._kernel
    _ = context._
    # app = context.app
    # print (f"Received context: {vars(context)}")
    # The main interface for creation

    def display_config_dialog(context, coolid):
        dialog = ConfigDialog(context, coolid, wx.ID_ANY, "")
        if dialog.ShowModal() == wx.ID_OK:
            pass
        dialog.Destroy()

    @kernel.console_argument("coolid", type=str, help=_("The specific configuration to edit"))
    @kernel.console_command(
        "coolant_config_mqtt",
        help=_("Allows the configuration and addition of mqtt interfaces for coolant support."),
        input_type=None,
        output_type=None,
    )
    def open_config_dialog(
        command,
        channel,
        _,
        coolid=None,
        data=None,
        **kwargs,
    ):
        display_config_dialog(context, coolid)
        return None

    kernel.register("window/Airassist_mqtt", ConfigDialog)
