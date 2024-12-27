import sys
import json
import os
import re
import glob
# from mayavi import mlab
# import time_htht as htt
from toothedsword import time_htht as htt
import numpy as np
# import pandas as pd
import copy
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Cursor, Button, CheckButtons
# from osgeo import gdal
# from skimage import morphology
import time
from matplotlib import colors
from matplotlib import cm
from matplotlib import path
import matplotlib
import matplotlib.patheffects as path_effects


from matplotlib.font_manager import FontProperties
yh_font = FontProperties(fname='/usr/share/fonts/msyh.ttc')
kai_font = FontProperties(fname='/usr/share/fonts/simkai.ttf')
hei_font = FontProperties(fname='/usr/share/fonts/simhei.ttf')


def remove_white(figname, maxw=0.05, axis=0, outfile='', idy=''):
    im = plt.imread(figname).astype(np.float32)
    if str(type(idy)) == str(type('')):
        height, width = im.shape[0], im.shape[1]
        rgb = im[:,:,0]+im[:,:,1]+im[:,:,2]
        rgb[im[:,:,3] == 0] = 255 
        rgb = np.sum(rgb, 1-axis)
       
        w = im.shape[1-axis]*3*255
        w = np.max(rgb)
        rgb[0] = 0
        rgb[-1] = 0
        id = np.where(rgb < w)
        id = id[0]
        idb = id[1:] - id[0:-1]

        maxw = maxw * im.shape[axis]
        idb_gt_maxw = np.where(idb >  maxw)
        idb_gt_maxw = idb_gt_maxw[0]
        idy = rgb >= 0
        for i in idb_gt_maxw.tolist():
            idy[id[i]:id[i+1]] = False
            idy[id[i]:int(id[i]+maxw)] = True

    if axis == 0:
        im = im[idy, :, :]
    else:
        im = im[:, idy, :]
    
    if outfile == '':
        outfile = figname

    plt.imsave(outfile, np.ascontiguousarray(im))
    return idy


def figure(*args, add_axes=False, **kw):
    fig = plt.figure(*args, **kw, FigureClass=FIG)
    fig.plt = plt
    fig.yh_font = yh_font
    fig.kai_font = kai_font
    fig.hei_font = hei_font
    if add_axes:
        ax = fig.add_axes_auto()
        fig.ax = ax
    return fig


class FIG(plt.Figure):
    """Docstring for . """

    def init(self):
        self.fig_varname = 'xxx'
        self.dpi = 400
        self.fig_varunit = 'xxx'
        self.qgs_template = '/home/leon/src/qgisfig/new/achn/template.qgs'
        self.qgs_template = '/home/leon/src/qgisfig/glob/template.qgs'
        self.qgs_template = '/home/leon/src/qgis-050/dynamic-range/template.qgs'
        self.fontproperties = kai_font
        self.fontcolor = '#000000'
        self.pngfile = str(time.time())+'.png'
        self.png_json_file = self.pngfile + '.json'
        self.outfile = self.pngfile+'.png'
        self.time = time.time()
        self.ttl = 'xxxxx'
        self.sat = 'xxx'
        self.axpos = self.ax.get_position().bounds
        self.cb_axpos_out = [0,0,1,0.2]
        self.res = 'xxx'
        self.prodir = os.path.dirname(os.path.abspath(__file__))
        self.qgs_template_json = self.qgs_template + '.json'
        self.update_png_json = {}

    def fontzoom(self, scale):
        for text_obj in self.findobj(match=type(plt.Text)):
            try:
                text_obj.set_fontsize(text_obj.get_fontsize() * scale)
            except Exception as e:
                pass
                # print('---------------')
                # print(e)

    def remove_close_text(self, mindis, text_objs, rt='CC'):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        def dis(x1,y1,x0,y0,xlim,ylim):
            x1 = (x1 - xlim[0])/(xlim[1]-xlim[0])
            y1 = (y1 - ylim[0])/(ylim[1]-ylim[0])
            x0 = (x0 - xlim[0])/(xlim[1]-xlim[0])
            y0 = (y0 - ylim[0])/(ylim[1]-ylim[0])
            return np.sqrt((x1-x0)**2+(y1-y0)**2)

        for text_obj in text_objs:
            try:
                s0 = text_obj.get_text()
                x0, y0 = text_obj.get_position()
                if s0 == ' ':
                    continue
                
                for text_obj1 in text_objs:
                    try:
                        s1 = text_obj1.get_text()
                        x1, y1 = text_obj1.get_position()
                        d = dis(x1,y1,x0,y0,xlim,ylim)
                        if d > 0 and d < mindis and not(s1 == ' '):
                            text_obj1.set_text(' ')
                        
                    except Exception as e1:
                        print('---------------')
                        print(e1)
            except Exception as e:
                print('---------------')
                print(e)

    def add_axes_auto(self, type='main'):
        if type == 'main':
            ax = self.add_axes([0.15, 0.15, 0.7, 0.7])
            self.ax = ax

        if re.search('cb', type):
            if re.search('h', type):
                ax = self.add_axes([0.15, 0.15, 0.7, 0.02])
            else:
                ax = self.add_axes([0.87, 0.15, 0.02, 0.7])
            self.cax = ax
        return ax

    def set_timetick(self, xy='x', ss='yyyymmddHHMMSS'):
        ax = self.ax
        xticks = ax.get_xticks()
        xticklabels = []
        for x in xticks:
            xticklabels.append(htt.time2str(x, ss))
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)

    def add_space(self, dr, wd):
        ax = self.ax
        current_position = ax.get_position()
        current_position_list = [current_position.x0, current_position.y0, current_position.width, current_position.height]
        
        try:
            cax = self.cax
            cposition = cax.get_position()
            cposition_list = [cposition.x0, cposition.y0, cposition.width, cposition.height]
        except Exception as e:
            print(e)

        if dr == 'top':
            current_position_list[3] -= wd
            cposition_list[3] -= wd

        if dr == 'right':
            current_position_list[2] -= wd
            cposition_list[0] -= wd

        if dr == 'bottom':
            current_position_list[3] -= wd
            current_position_list[1] += wd
            cposition_list[3] -= wd
            cposition_list[1] += wd

        if dr == 'left':
            current_position_list[2] -= wd
            current_position_list[0] += wd

        ax.set_position(current_position_list)
        try:
            cax.set_position(cposition_list)
        except Exception as e:
            print(e)

    def save(self, *args, maxw=[1,1], **kw):
        self.savefig(*args, **kw)
        fname = args[0]
        remove_white(fname, maxw=maxw[0], axis=0)
        remove_white(fname, maxw=maxw[1], axis=1)

    def set_axes_thick(self, thick):
        # for ax in self.axes:
        for ax in self.get_axes():
            # 获取当前Axes对象的边框
            spines = ax.spines

            # 设置边框线宽度为3
            for spine in spines.values():
                spine.set_linewidth(thick)

    def add_colorbar(self):
        self.ax_cb = self.fig.add_axes(self.cb_axpos_in)
        cb = plt.colorbar(self.it, cax=self.ax_cb, 
                orientation='horizontal')

    def copy_attr_from_parent(self):
        pass


    def add_ll_unit_ax(self):
        # {{{
        ax = self.ax
        ts = []
        for t in ax.get_xticklabels():
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'$^{o}$W'
            else:
                t1 = t.get_text()+'$^{o}$E'
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

        ts = []
        for t in ax.get_yticklabels():
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'$^{o}$S'
            else:
                t1 = t.get_text()+'$^{o}$N'
            ts.append(t1)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ts)
        # }}}


    def add_tick_space(self, xy):
        # {{{
        ax = self.ax
        ts = []
        it = 1
        for t in ax.get_xticklabels():
            it += 1
            t1 = t.get_text()+''
            if xy[0] > 0:
                if it % xy[0] == 1:
                    pass
                else:
                    t1 = ' '
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

        ts = []
        it = 0
        for t in ax.get_yticklabels():
            it += 1
            t1 = t.get_text()+''
            if xy[1] > 0:
                if it % xy[1] == 1:
                    t1 = ' '
            ts.append(t1)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ts)
        # }}}

    def add_ll_unit_ax1(self):
        # {{{
        ax = self.ax
        ts = []
        it = 1
        for t in ax.get_xticklabels():
            it += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'W'
            else:
                t1 = t.get_text()+'E'
            if it % 3 == 1:
                pass
            else:
                t1 = ' '
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

        ts = []
        it = 0
        for t in ax.get_yticklabels():
            it += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'S'
            else:
                t1 = t.get_text()+'N'
            if it % 2 == 1:
                t1 = ' '
            ts.append(t1)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ts)
        # }}}

    def add_ll_unit_ax2(self):
        # {{{
        ax = self.ax
        ts = []
        it = 1
        for t in ax.get_xticklabels():
            it += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'W'
            else:
                t1 = t.get_text()+'E'
            if it % 2 == 1:
                pass
            else:
                t1 = ' '
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

        ts = []
        it = 0
        for t in ax.get_yticklabels():
            it += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'S'
            else:
                t1 = t.get_text()+'N'
            if it % 2 == 1:
                t1 = ' '
            ts.append(t1)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ts)
        # }}}


    def add_ll_unit_ax0(self):
        # {{{
        ax = self.ax
        ts = []
        it = 1
        for t in ax.get_xticklabels():
            it += 1
            t1 = t.get_text()+''
            if it % 2 == 1:
                pass
            else:
                t1 = ' '
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

        ts = []
        it = 0
        for t in ax.get_yticklabels():
            it += 1
            t1 = t.get_text()+''
            if it % 2 == 1:
                t1 = ' '
            ts.append(t1)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ts)
        # }}}


    def set_fmt_ax(self):
        ax = self.ax
        ts = []
        i = 0
        for t in ax.get_xticklabels():
            i += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'$^{o}$S'
            else:
                t1 = t.get_text()+'$^{o}$N'
            t1 = re.sub(r'(\d.\d)\d*', r'\1', t1)
            if i % 2 == 1:
                t1 = ' '
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

    def save_png(self):
        # {{{
        pngfile = self.pngfile
        fig = self
        ax = self.ax
        ax_cb = self.ax_cb
        ym = ax_cb.get_ylim()
        xm = ax_cb.get_xlim()
        dy = ym[1]-ym[0]

        ax_cb.text(xm[0], ym[0]+dy/2, self.fig_varname+'  ', fontproperties=self.fontproperties,
                horizontalalignment='right', verticalalignment='center')
        ax_cb.text(xm[1], ym[0]+dy/2, '  '+self.fig_varunit, fontproperties=yh_font,
                horizontalalignment='left', verticalalignment='center')


        if self.fontcolor == '#ffffff':
            fe = [path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()]
            for tax in [ax, ax_cb]: 
                # {{{
                ts = tax.get_children()
                ts.extend(tax.get_xticklabels())
                for t in ts:
                    try:
                        if re.search(r'Text', str(type(t))):
                            t.set_path_effects(fe)
                            t.set_color('w')
                    except Exception as e:
                        print(e)
                        # }}}

        outdir = re.sub(r'[^\/]+$', '', self.outfile)
        os.system('mkdir -p '+outdir)
        fig.savefig(pngfile, transparent=True, dpi=self.dpi)
        # }}}

    def gen_png_dict(self):
        # {{{
        fig = self
        ax = self.ax
        ax_cb = self.ax_cb
        self.textspan0 = ''
        self.textspan1 = ''

        if self.fontcolor == '#ffffff':
            self.textspan0 = '<p style="color:'+self.fontcolor+\
                    ';-webkit-text-stroke: 4px black">'
            self.textspan1 = '</p>'

        stime = htt.time2str(self.time, 'yyyymmddHHMMSS')
        outfile = self.outfile

        outdir = re.sub(r'[^\/]+$', '', outfile)
        os.system('mkdir -p '+outdir)
        lonlim = ax.get_xlim()
        latlim = ax.get_ylim()

        pngdict = {'title': self.textspan0+self.ttl+self.textspan1, 
                   'date': self.textspan0+htt.time2str(self.time+8*3600, 'yyyy-mm-dd HH:MM')+'(北京时间)'+self.textspan1,
                   'lonlim': [lonlim[0], lonlim[1]], 
                   'latlim': [latlim[0], latlim[1]], 
                   'qgsfile': outfile,
                   'satellite': self.textspan0+'卫星: '+self.sat+self.textspan1,
                   'axpos': self.axpos,
                   'cbpos': self.cb_axpos_out,
                   "tuli": self.textspan0+"图 例"+self.textspan1,
                   "guojie": self.textspan0+"国界"+self.textspan1,
                   "shengjie": self.textspan0+"省界"+self.textspan1,
                   "haiyang": self.textspan0+"海洋"+self.textspan1,
                   "ludi": self.textspan0+"陆地"+self.textspan1,
                   'resolution': self.textspan0+'分辨率: '+self.res+self.textspan1}
        try:
            pngdict['date'] = self.textspan0+self.rttl+self.textspan1
        except Exception as e:
            print(e)
        try:
            for k in self.pngdict_add.keys():
                pngdict[k] = self.pngdict_add[k]
        except Exception as e:
            pass
        for k in pngdict.keys():
            try:
                if re.search(r'^###', pngdict[k]):
                    pngdict[k] = self.textspan0+\
                            re.sub(r'^###', self.textspan0, 
                                    pngdict[k])+self.textspan1
            except Exception as e:
                print(e)
        self.pngdict = pngdict
        # }}}

    def save_png_json(self):
        # {{{
        pngfile = self.pngfile
        png_json_file = pngfile+'.json'

        if self.png_json_file == '':
            pass
        else:
            png_json_file = self.png_json_file
        with open(png_json_file, "w", encoding='utf-8') as f:
            json.dump(self.pngdict, f)
        self.png_json_file = png_json_file
        # }}}

    def gen_qgis(self):
        # {{{
        pngfile = self.pngfile

        cmd = 'python3 '+self.prodir+'/../png2qgis/exe_png2qgis.py --png='+pngfile+' --qgs='+self.qgs_template+' --png_json='+self.png_json_file
        if self.qgs_template_json == '':
            pass
        else:
            cmd += ' --qgs_json='+self.qgs_template_json
        print(cmd)
        os.system(cmd)
        pass
        # }}}

    def save2qgis(self):
        self.save_png()
        self.gen_png_dict()
        try:
            if self.removeout:
                self.pngdict.update({'removeout':'yes'})
        except Exception as e:
            print(e)
        try:
            if self.maxw0 > 0:
                self.pngdict.update({'maxw0':self.maxw0})
        except Exception as e:
            print(e)
        try:
            if self.maxw1 > 0:
                self.pngdict.update({'maxw1':self.maxw1})
        except Exception as e:
            print(e)
        self.pngdict.update(self.update_png_json)
        self.save_png_json()
        self.gen_qgis()
        # os.system('rm -rf '+self.pngfile+'.*')


def fontzoom(obj, scale):
    for text_obj in obj.findobj(match=type(plt.Text)):
        try:
            text_obj.set_fontsize(text_obj.get_fontsize() * 2)
        except Exception as e:
            print(e)


def main():
    fig = figure()
    ax = fig.add_axes([0.1,0.3,0.8,0.7])
    it = ax.imshow([[0,1],[3,4]], extent=[70, 150, 0, 70])

    cax = fig.add_axes([0.3,0.1,0.6,0.02])
    fig.plt.colorbar(it, cax=cax)

    fig.ax, fig.it, fig.ax_cb = ax, it, cax
    fig.init()
    fig.update_png_json['extent'] = [100, 150, 0, 50]
    fig.save2qgis()

def main1():
    fig = figure()
    ax = fig.add_axes([0.1,0.3,0.8,0.7])
    import numpy as np

    t = np.arange(10000).reshape(100, 100)
    it = ax.imshow(t, extent=[70, 150, 0, 70])

    cax = fig.add_axes([0.3,0.1,0.6,0.02])
    fig.update_png_json['extent'] = [100, 150, 0, 50]
    fig.plt.colorbar(it, cax=cax)

    fig.ax, fig.it, fig.ax_cb = ax, it, cax
    fig.init()
    fig.update_png_json['extent'] = [100, 150, 0, 50]
    fig.update_png_json['extent'] = [100, 150, 0, 50]
    fig.save2qgis()


def test():
    fig = figure()
    ax = fig.add_axes([0.1, 0.3, 0.8, 0.7])

    it = ax.imshow([[0,1],[3,4]], extent=[70, 150, 0, 70])

    cax = fig.add_axes([0.3,0.1,0.6,0.02])
    fig.plt.colorbar(it, cax=cax, orientation='horizontal')

    fig.ax, fig.it, fig.ax_cb = ax, it, cax
    fig.init()
    fig.update_png_json['qgslevel'] = 3
    fig.qgs_template = './achn/template.qgs'
    fig.qgs_template_json = './achn/template.qgs.json'
    fig.save2qgis()


def test0():
    fig = figure()
    ax = fig.add_axes([0.1, 0.3, 0.8, 0.7])

    it = ax.imshow([[0,1],[3,4]], extent=[70, 150, 0, 70])

    cax = fig.add_axes([0.3,0.1,0.6,0.02])
    fig.plt.colorbar(it, cax=cax, orientation='horizontal')

    fig.ax, fig.it, fig.ax_cb = ax, it, cax
    fig.init()
    fig.qgsfile = '/tmp/1.png'
    fig.update_png_json = {'qgslevel':12}
    fig.qgs_template = './achn/template.qgs'
    fig.qgs_template_json = './achn/template.qgs.json'
    fig.save2qgis()


def test1():
    fig = figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax = imshow([[1,2],[3,4]])
    ax.plot([1,2,3])

    fig.int()
    fig.update_png_json()
    fig.save2qgis()

if __name__ == "__main__":
    test()

