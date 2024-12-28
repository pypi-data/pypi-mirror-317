def main():
    
    '''  Description of custom_print project  '''
    from custom_print import FancyFormat
    lst = [["Module Name",         "custom_print"                          ],
           ["Version",             "0.0.8"                                 ],
           ["Author",              "Miguel Angel Aguilar Cuesta"           ],
           ["Author Email",        "acma.mex@gmail.com"                    ],
           ["Description",         "Customized Print"                      ],
           ["Long Description",    "README.md"                             ],
           ["Content Type",        "MarkDown"                              ],
           ["Find README.md at",   "https://github.com/acma82/Custom_Print"],
           ["Dependencies",        "None"                                  ],
           ["License",             "Everyone Can Use It"                   ]]

    tbl = FancyFormat()
    # FACE = "(" + chr(0x25D5) + chr(0x25E1) + chr(0x25D5) + ")"
    FACE = "(" + "0" + chr(0x25E1) + "0" + ")"
    tbl.msg_title = FACE + "  Project Description"
    tbl.msg_footnote = "Released on Friday, December 27, 2024"
    tbl.align_title = "center"
    tbl.adj_top_space = 1;          tbl.adj_bottom_space = 1

    # bg colors
    tbl.bg_horizontal_line = 21;    tbl.bg_inner_corner_chr  = 21
    tbl.bg_vertical_line   = 21;    tbl.bg_under_line_header = 21
    tbl.bg_corner_chr      = 21;    tbl.adj_bottom_margin = 2

    tbl.bg_corner_under_line_header = 21
    tbl.bg_vertical_header_line_chr = 21

    tbl.bg_header = 52;             tbl.bg_data = 231
    tbl.fg_header = 231;            tbl.fg_data = 0
    tbl.bold_header = True;         tbl.bold_data = True
    tbl.adj_top_margin = 2;         tbl.adj_indent = 4

    tbl.print_fancy_format(lst, "no_space_col_color")
