jQuery(function($){
        
        $.supersized({
        
          // Functionality

          slide_interval          :   120000,   // Length between transitions
          transition              :   1,      // 0-None, 1-Fade, 2-Slide Top, 3-Slide Right, 4-Slide Bottom, 5-Slide Left, 6-Carousel Right, 7-Carousel Left
          transition_speed    : 700,    // Speed of transition
                                 
          // Size & Position               
          min_width           :   0,      // Min width allowed (in pixels)
          min_height            :   0,      // Min height allowed (in pixels)
          vertical_center         :   1,      // Vertically center background
          horizontal_center       :   1,      // Horizontally center background
          fit_always        : 0,      // Image will never exceed browser width or height (Ignores min. dimensions)
          fit_portrait          :   1,      // Portrait images will not exceed browser height
          fit_landscape     :   0,      // Landscape images will not exceed browser width
                                 
          // Components
          slides          :   [     // Slideshow Images
                            {image : '/media/supersized/bgs/kflood.jpg'},
                            {image : '/media/supersized/bgs/kruger.jpg'},
                            {image : '/media/supersized/bgs/kflood2.jpg'}
                        ]
          
        });
        });