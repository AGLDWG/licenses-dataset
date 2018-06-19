from model import sparql
from pyldapi import *


class OdrlPoliciesObjectRenderer(Renderer):
    def __init__(
            self,
            request,
            uri,
            label,
            comment,
            views,
            default_view_token
            ):
        super().__init__(
            request,
            uri,
            views,
            default_view_token
        )
        self.label = label
        self.comment = comment

    def render(self):
        if hasattr(self, 'vf_error'):
            return Response(self.vf_error, status=406, mimetype='text/plain')
        else:
            if self.view == 'alternates':
                return self._render_alternates_view()
            elif self.view == 'pol':
                return self._render_pol_view()

    def _render_pol_view(self):
        if self.format in Renderer.RDF_MIMETYPES:
            rdf = sparql.object_describe(self.uri, self.format)
            if rdf is None:
                return Response('No triples contain that URI as subject', status=404, mimetype='text/plain')
            else:
                return Response(rdf, mimetype=self.format)
        else:  # only the HTML format left
            deets = sparql.instance_details(self.uri)
            if deets is None:
                return Response('That URI yielded no data', status=404, mimetype='text/plain')
            else:
                return render_template(
                    'object.html',
                    deets=deets
                )