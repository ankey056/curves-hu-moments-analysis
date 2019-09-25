
import subprocess as sp

class InkShell:
    def __init__(self):
        "Open unbuffered pipe to Inkscape process"
        self.p = sp.Popen(['inkscape', '--shell'], 
                          bufsize=0, universal_newlines=True,
                          stdin=sp.PIPE, stdout=sp.PIPE)
        self.read()

    def read(self):
        "Read stdout from Inkscape"
        rv = ''
        while True:
            r = self.p.stdout.read(1)
            if r == '>':
                break
            rv += r
        return rv

    def write(self, words_of_wisdom):
        "Write data and newline char"
        return self.p.stdin.write(words_of_wisdom + '\n')
    
    def close(self):
        "Terminate Inkscape process"
        stdout, stderr = self.p.communicate('quit\n')
        return self.p.returncode, stdout, stderr

    def _query_param (self, svgfile, id, p):
        com = svgfile + " --query-id " + id + " --query-" + p
        
        self.write(com)
                                     
        return float(self.read())

    def get_svg_geometry (self, svgfile, id=None):
        """Return parameters list [xposition, yposition, width, height] of svg or,
        if id is not None, of object that is defined by id."""
        com = svgfile
        
        if id: 
            return map(lambda p: self._query_param(svgfile, id, p),
                       ("x", "y","width", "height"))
        else:
            self.write(com + " --query-all")
            s = self.read().splitlines()[0]
            return map(float,s.split(',')[1:])

    def export_svg_in_png (self, svg, pngout, svgarea=None,
                           width=None, height=None,
                           bg=None, id_only=None):
        com = svg
        com += " --export-png={0}".format(pngout)
        if svgarea:
            com += " --export-area={0}".format(':'.join(map(str,svgarea)))
        if bg:
            com += " --export-background='{0}'".format(bg)

        if height: com += " --export-height={0}".format(height)
        if width: com += " --export-width={0}".format(width)
        if id_only:
            com += " --export-id-only --export-id={0}".format(id_only)
            
        self.write(com)
        self.read()
        return pngout

    def export_svg_object_in_png (self, svg, vby, pngout, id,
                                  width=None, height=None,
                                  bg=None, expansion=None,
                                  rcoefs=None):
        x,y,w,h = self.get_svg_geometry(svg, id=id)
        
        dx = 0
        x1 =  x
        x2 =  x + w
        y1 = vby - y + h/3.0
        y2 = y1 + h
        # print "file:{}\n vby:{}, y:{}, h:{}".format(pngout, vby, y, h)

        if expansion:
            p = (expansion - 1) / 2
            dx = w * p
            dy = h * p
            x1-= dx
            x2+= dx
            y1-= dy
            y2+= dy

        if False: #rcoefs:
            kw, kh = rcoefs
            width = int(round((kw * (x2 - x1))))
            height = int(round((kh * (y1 - y2))))

        return self.export_svg_in_png(svg,  pngout, svgarea=(x1,y1,x2,y2),
                                      width=width, height=height,
                                      bg=bg, id_only=id)
