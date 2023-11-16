PAGE = """
@page {{size: A4 Potrait;
	margin: 1.5cm 1.27cm 1.75cm 1.27cm;
  @top-left {{
    content: '{top_left}';
	  word-wrap: break-word;
    font-size: 13px;
    height: 1cm;
    vertical-align: middle;
    width: 80%;
    opacity: .9;
	  margin-bottom:0.17cm;
  }}
  @top-center {{
    background: #F97D09;
    content: '';
    display: block;
    height: .05cm; 
    opacity: .5;
    width: 100%;
  margin-bottom:0.25cm;
  }}
  @top-right {{
    content: '{top_right}';
	word-wrap: break-word;
    font-size: 13px;
    height: 1cm;
    vertical-align: middle;
    width: 80%;
    opacity: .9;
	margin-bottom:0.17cm;
  }}
 @bottom-left {{
    content: '{bottom_left}';
    font-size: 13px;
    opacity: .8;
  }} 
@bottom-right {{
	content :'{bottom_right}';
}}
}}
"""

