# from unittest.mock import MagicMock
#
# from kivy.tests.common import GraphicUnitTest
# from kivy.lang import Builder
# from menu import MenuWidget
#
#
# class TestMenuWidget(GraphicUnitTest):
#
#     def test_menu_widget_opacity(self):
#         """Test that the MenuWidget handles touch events based on its opacity."""
#         # Load the widget
#         menu_widget = MenuWidget()
#
#         # Set opacity to 0 and test touch behavior
#         menu_widget.opacity = 0
#         touch = self.create_touch(menu_widget.center_x, menu_widget.center_y)
#
#         # Render the widget
#         self.render(menu_widget)
#
#         # Simulate touch down and ensure it returns False
#         assert not menu_widget.on_touch_down(touch), "Widget should not handle touches when opacity is 0"
#
#         # Now test with opacity set to 1
#         menu_widget.opacity = 1
#         touch = self.create_touch(menu_widget.center_x, menu_widget.center_y)
#
#         # Simulate touch down and ensure it returns True (handled by parent)
#         assert menu_widget.on_touch_down(touch), "Widget should handle touches when opacity is 1"




# class TestMainWidget(GraphicUnitTest):
#
#     # def test_main_widget_initialization(self):
#     #     """Test the initialization of the MainWidget."""
#     #     # Load the main widget
#     #     main_widget = MainWidget()
#     #
#     #     # Render the widget
#     #     self.render(main_widget)
#     #
#     #     # Check if important elements are initialized (e.g., the ship)
#     #     assert main_widget.ship is not None, "Ship should be initialized"
#
#     # def test_main_widget_interactions(self):
#     #     """Test interactions with the MainWidget sans modifier le code principal."""
#     #     main_widget = MainWidget()
#     #
#     #     # Mock des attributs de dimensions et point_perspective_y pour éviter ZeroDivisionError
#     #     main_widget.width = 100
#     #     main_widget.height = 100
#     #     main_widget.point_perspective_y = 50  # Valeur non nulle pour éviter ZeroDivisionError
#     #
#     #     # Simuler le rendu du widget
#     #     self.render(main_widget)
#     #
#     #     # Simuler une interaction de type touch
#     #     touch = MagicMock()  # Mock de l'événement touch
#     #     main_widget.on_touch_down(touch)
#     #
#     #     # Vérifier que l'événement touch est correctement géré
#     #     assert main_widget.collide_point(touch.x, touch.y), "Le touch event n'a pas été géré correctement."