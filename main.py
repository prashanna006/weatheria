from flet import *
from backend import get_weather

# App Dimensions
width = 400
height = 800

# Colors
body_color = '#15719f'
app_icon_color = colors.AMBER
app_title_color = colors.WHITE
search_bar_color = '#91cfec'
search_icon_color = '#000000'
transparent_black = colors.with_opacity(0.25, '#000000')
divider_color = '#000000'
sunrise_gradient = [colors.AMBER_200, '#FFC107', '#FFEB3B']
sunset_gradient = ['#000033', '#001A66', '#001F54']


def main(page: Page):
    def on_resize(event):
        width = page.window_width
        height = page.window_height
        print(width, height)
    
    # Page Settings
    page.window_width = 440
    page.window_height = 860
    page.title = "Weatheria"
    page.scroll = "auto"
    page.on_resize = on_resize
    page.window_always_on_top = True
    
    # Title Section
    
    app_icon = Icon(
        icons.SUNNY, color=app_icon_color, size=30
    )
    
    app_title = Text(
        "Weatheria", color=app_title_color, size=25, weight='w500'
    )
    
    # Centered Title Row
    title_bar = Container(
        content=Row(
            controls=[
                app_title,
                app_icon
            ],
            alignment=MainAxisAlignment.CENTER,  # Center within the Row
            vertical_alignment=CrossAxisAlignment.CENTER  # Center vertically
        ),
        alignment=alignment.center  # Center the container itself
    )
    
    # Define individual components with identifiers
    city_field = TextField(
        label="City Name", hint_text="Seattle", text_align=TextAlign.LEFT, width=width / 1.5,
        border_color=search_bar_color, border_width=2.5, border_radius=10
    )

    section_divider = Divider(
        color=divider_color,
        leading_indent=10,
        trailing_indent=10,
        height=3,
        thickness=2
    )

    invisible_divider = Divider(
        color=colors.TRANSPARENT,
        thickness=5
    )

    city_name = Text(value="City_Name", size=25, weight='w300')
    city_name_box = Container(
        content=city_name,
        padding=padding.only(left=width / 16, bottom=-height / 85)
    )

    location_icon = Container(
        content=Icon(
            icons.LOCATION_ON_OUTLINED, color='white', size=25
        ), 
        padding=padding.only(left=-width / 40, bottom=-height / 85)
    )

    current_temp = Text(value=f"--\u00B0F", size=45)
    current_temp_info = Container(
        content=current_temp,
        padding=padding.only(top=-height / 85, left=width / 16),
        width=150
    )

    max_temp = Text(value=f"--\u00B0F", size=20, text_align=TextAlign.CENTER)
    min_temp = Text(value=f"--\u00B0F", size=20, text_align=TextAlign.CENTER)
    min_max_temp_container = Container(
        width=width / 5, height=width / 5,  # Adjust height to give more room for text
        bgcolor=transparent_black,
        border_radius=10,
        padding=padding.only(left=width / 3.3)
    )

    min_max_temp_info = Container(
        content=Stack(
            controls=[
                min_max_temp_container,
                Container(
                    content=max_temp,
                    padding=padding.only(top=5),
                    width=min_max_temp_container.width, height=min_max_temp_container.height, alignment=alignment.top_center
                ),
                Container(
                    content=min_temp,
                    padding=padding.only(bottom=5),
                    width=min_max_temp_container.width, height=min_max_temp_container.height, alignment=alignment.bottom_center
                ),
            ]
        ),
        padding=padding.only(left=width / 3.3)
    )


    weather_desc = Text(value="Weather Desc.", size=17, weight='w600')
    weather_desc_info = Container(
        content=weather_desc,
        padding=padding.only(left=width / 16, top=-height / 34)
    )
    
    feels_like = Text(value = f"Feels like --\u00B0F", size = 17, weight = 'w600')
    feels_like_info = Container(
        content=feels_like,
        padding=padding.only(left=width / 16, top=-height / 75)
    )

    sunrise_box = Container(
        width=width * 0.40,
        height=height / 10,
        gradient=LinearGradient(
            begin=alignment.center_left,
            end=alignment.center_right,
            colors=sunrise_gradient,
            tile_mode=GradientTileMode.CLAMP
        ),
        border_radius=15 
    )
    sunrise_text = Container(Text("Sun Rise", color=sunset_gradient[2], size=17, weight='w600'), width=sunrise_box.width,
                             height=sunrise_box.height, alignment=alignment.top_center)
    sunrise = Text(f"--:-- AM", color=sunset_gradient[2], size=25)
    sunrise_stack = Stack([
        sunrise_box,
        sunrise_text,
        Container(sunrise, padding.only(top=10), alignment=alignment.center,
                  width=sunrise_box.width, height=sunrise_box.height,)
    ])
    
    sunset_box = Container(
        width=width * 0.40,
        height=height / 10,
        gradient=LinearGradient(
            begin=alignment.center_left,
            end=alignment.center_right,
            colors=[
                "#000033",   # Deep dark blue as the starting color
                "#001A66",   # Intermediate dark blue for a smooth transition
                "#001F54"    # Navy blue as the final color
            ],
            tile_mode=GradientTileMode.CLAMP  # Smoothly extends gradient
        ),
        border_radius=15  # Optional: soften corners for a modern look
    )
    sunset_text = Container(Text("Sun Set", color=sunrise_gradient[2], size=17, weight='w600'), width=sunrise_box.width,
                             height=sunrise_box.height, alignment=alignment.top_center)
    sunset = Text(f"--:-- PM", color=sunrise_gradient[2], size=25)
    sunset_stack = Stack([
        sunset_box,
        sunset_text,
        Container(sunset, padding.only(top=10), alignment=alignment.center,
                  width=sunset_box.width, height=sunset_box.height)
    ])


    common_info_box = Container(
        width=width * 0.40,
        height=height / 13,
        bgcolor=transparent_black,
        border_radius=25,
    )

    wind_info_icon = Container(
        Icon(icons.AIR, size=24), padding=padding.only(left=10, top=10)
    )

    wind_info_text = Container(
        Text("Wind Speed", size=15, weight='w300'), padding=padding.only(left=-5, top=10)
    )

    # Create the Text object separately to easily update it
    wind_info = Text(f"-- km/hr", text_align=TextAlign.LEFT, weight='w600', size=20)
    wind_info_box = Container(
        wind_info,
        padding=padding.only(top=height / 30, left=25),
        alignment=alignment.center_left
    )

    wind_stack = Container(
        Stack(
            [
                common_info_box,
                Row([wind_info_icon, wind_info_text]),
                wind_info_box,
            ]
        )
    )

    humidity_info_icon = Container(
        Icon(icons.GRAIN, size=24), padding=padding.only(left=10, top=10)
    )

    humidity_info_text = Container(
        Text("Humidity", size=15, weight='w300'), padding=padding.only(left=-5, top=10)
    )

    # Create the Text object separately to easily update it
    humidity_info = Text(f"-- km/hr", text_align=TextAlign.LEFT, weight='w600', size=20)
    humidity_info_box = Container(
        humidity_info,
        padding=padding.only(top=height / 30, left=25),
        alignment=alignment.center_left
    )

    humidity_stack = Container(
        Stack(
            [
                common_info_box,
                Row([humidity_info_icon, humidity_info_text]),
                humidity_info_box,
            ]
        )
    )


    pressure_info_icon = Container(
        Icon(icons.SPEED, size=24), padding=padding.only(left=10, top=10)
    )

    pressure_info_text = Container(
        Text("Pressure", size=15, weight='w300'), padding=padding.only(left=-5, top=10)
    )

    # Create the Text object separately to easily update it
    pressure_info = Text(f"-- km/hr", text_align=TextAlign.LEFT, weight='w600', size=20)
    pressure_info_box = Container(
        pressure_info,
        padding=padding.only(top=height / 30, left=25),
        alignment=alignment.center_left
    )

    pressure_stack = Container(
        Stack(
            [
                common_info_box,
                Row([pressure_info_icon, pressure_info_text]),
                pressure_info_box,
            ]
        )
    )


    visibility_info_icon = Container(
        Icon(icons.REMOVE_RED_EYE, size=24), padding=padding.only(left=10, top=10)
    )

    visibility_info_text = Container(
        Text("Visibility", size=15, weight='w300'), padding=padding.only(left=-5, top=10)
    )

    # Create the Text object separately to easily update it
    visibility_info = Text(f"-- km/hr", text_align=TextAlign.LEFT, weight='w600', size=20)
    visibility_info_box = Container(
        visibility_info,
        padding=padding.only(top=height / 30, left=25),
        alignment=alignment.center_left
    )

    visibility_stack = Container(
        Stack(
            [
                common_info_box,
                Row([visibility_info_icon, visibility_info_text]),
                visibility_info_box,
            ]
        )
    )


    sea_lvl_info_icon = Container(
        Icon(icons.WATER, size=24), padding=padding.only(left=10, top=10)
    )

    sea_lvl_info_text = Container(
        Text("Sea Level", size=15, weight='w300'), padding=padding.only(left=-5, top=10)
    )

    # Create the Text object separately to easily update it
    sea_lvl_info = Text(f"-- km/hr", text_align=TextAlign.LEFT, weight='w600', size=20)
    sea_lvl_info_box = Container(
        sea_lvl_info,
        padding=padding.only(top=height / 30, left=25),
        alignment=alignment.center_left
    )

    sea_lvl_stack = Container(
        Stack(
            [
                common_info_box,
                Row([sea_lvl_info_icon, sea_lvl_info_text]),
                sea_lvl_info_box,
            ]
        )
    )


    ground_lvl_info_icon = Container(
        Icon(icons.GRASS, size=24), padding=padding.only(left=10, top=10)
    )

    ground_lvl_info_text = Container(
        Text("Ground Level", size=15, weight='w300'), padding=padding.only(left=-5, top=10)
    )

    # Create the Text object separately to easily update it
    ground_lvl_info = Text(f"-- km/hr", text_align=TextAlign.LEFT, weight='w600', size=20)
    ground_lvl_info_box = Container(
        ground_lvl_info,
        padding=padding.only(top=height / 30, left=25),
        alignment=alignment.center_left
    )

    ground_lvl_stack = Container(
        Stack(
            [
                common_info_box,
                Row([ground_lvl_info_icon, ground_lvl_info_text]),
                ground_lvl_info_box,
            ]
        )
    )



    # Arrange weather info fields in a Column
    weather_info_fields = Column([
        Row([wind_stack, humidity_stack], alignment=MainAxisAlignment.CENTER),
        Row([pressure_stack, visibility_stack], alignment=MainAxisAlignment.CENTER),
        Row([sea_lvl_stack, ground_lvl_stack], alignment=MainAxisAlignment.CENTER),
    
    ])
    error_text = Text(f"", color=colors.BLACK, size = 20)
    error_box = Container(error_text, padding.only(top = 40))
    
    all_values = [city_field, city_name, current_temp, max_temp, min_temp, weather_desc, feels_like, sunrise, sunset, wind_info, humidity_info, pressure_info, visibility_info, sea_lvl_info, ground_lvl_info, error_text]

    search_bar = Container(
        content=city_field,
        padding=padding.only(top=10)
    )

    search_button_icon = IconButton(
        icon=icons.SEARCH, icon_color=search_icon_color, bgcolor=transparent_black, on_click= lambda e: get_weather(all_values)
    )
    search_button = Container(
        content=search_button_icon,
        padding=padding.only(top=10)
    )
    
    # Weather App
    weather_page = Container(
        content=Column(
            controls=[
                Row(
                    [title_bar],
                    alignment=MainAxisAlignment.CENTER
                ),
                
                Row(
                    [search_bar, search_button],
                    alignment=MainAxisAlignment.CENTER,
                ),
                
                section_divider,
                
                Row([city_name_box, location_icon], alignment=MainAxisAlignment.START),
                
                Row([current_temp_info, min_max_temp_info]),
                
                Row([weather_desc_info,]),
                Row([feels_like_info]),
                
                invisible_divider,
                
                Row([sunrise_stack, sunset_stack], alignment=MainAxisAlignment.CENTER),
                
                invisible_divider,
                
                weather_info_fields,
                
                Row([error_box], alignment=MainAxisAlignment.CENTER),
            ]
        ),
    )
    
    body = Container(
        width=width,
        height=height,
        bgcolor=body_color,
        border_radius=15,
        ink=True,
        on_click=lambda e: None,
        padding=padding.only(top=25),
        content=Column(
            controls=[weather_page]
        )
    )
    
    page.add(body)

app(target=main)
