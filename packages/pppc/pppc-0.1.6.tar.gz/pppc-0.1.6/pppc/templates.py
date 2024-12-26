"""Template strings for Java code generation"""

MAIN_CLASS_TEMPLATE = '''
package {package_name};

import org.bukkit.plugin.java.JavaPlugin;

public class {class_name} extends JavaPlugin {{
    @Override
    public void onEnable() {{
        // Plugin startup logic
        {startup_code}
    }}

    @Override
    public void onDisable() {{
        // Plugin shutdown logic
        {shutdown_code}
    }}
}}
'''

EVENT_HANDLER_TEMPLATE = '''
@EventHandler
public void on{event_name}({event_type} event) {{
    {handler_code}
}}
'''

COMMAND_HANDLER_TEMPLATE = '''
@Override
public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {{
    {handler_code}
    return true;
}}
'''