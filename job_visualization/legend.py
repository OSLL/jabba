
import graphviz as gv

class Legend(object):
    def __init__(self):
        # Legend is presented as map (name -> settings)
        self.items = {}

    def add_item(self, name, settings):
        self.items[name] = settings

    def render(self):
        legend = gv.Digraph('cluster_legend')
        legend.body.extend(['label="Legend"'])

        for name, settings in self.items.items():
            legend.node("{}-1".format(name), label="")
            legend.node("{}-2".format(name), label="")

            legend.edge("{}-1".format(name), "{}-2".format(name), label=name, **settings)

        legend_wrapper = gv.Digraph('cluster_legend_wrapper')
        legend_wrapper.subgraph(legend)

        legend_wrapper.body.extend(['style=invis'])

        return legend_wrapper
