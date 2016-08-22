from tethys_sdk.base import TethysAppBase, url_map_maker


class ConstructionDewateringTool(TethysAppBase):
    """
    Tethys app class for Construction Dewatering Tool.
    """

    name = 'Construction Dewatering Tool (AEM)'
    index = 'timmldewater:home'
    icon = 'timmldewater/images/icon.gif'
    package = 'timmldewater'
    root_url = 'timmldewater'
    color = '#f1c40f'
    description = 'Simple tool for simulating the water table drawdown due to a system of wells surrounding an excavation. Model uses TimML to model groundwater behavior.'
    enable_feedback = False
    feedback_emails = []

        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='timmldewater',
                           controller='timmldewater.controllers.home'),
                    UrlMap(name='get_generate_water_table_ajax',
                           url='timmldewater/generate-water-table',
                           controller='timmldewater.controllers.generate_water_table'),
        )

        return url_maps