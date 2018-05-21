# Licenses Linked Data Dataset
A Linked Data dataset of licenses presented as Policies according to the [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/).

This dataset contains representations of licenses, such as the well known [Creative Commons BY 4.0](https://creativecommons.org/licenses/by/4.0) and the far less well known or used [Yancoal Pty Ltd Gloucester Licence](http://data.bioregionalassessments.gov.au/id/licence/559d2c0f898c0a477b44f7de), according to the ODRL Information Model. This representation interprets each license as a [`Policy`](https://www.w3.org/TR/odrl-vocab/#term-Policy) which then allows one or more [`Rule`](https://www.w3.org/TR/odrl-vocab/#term-Rule) objects in the form of a [`Duty`](https://www.w3.org/TR/odrl-vocab/#term-Duty), [`Permission`](https://www.w3.org/TR/odrl-vocab/#term-Permission), or [`Prohibition`](https://www.w3.org/TR/odrl-vocab/#term-Prohibition), to be associated with it. These associations then indicate actions that may be required of, or permitted to, or required not to be performed by, parties bound by the policy, i.e. users of data who have agreed to the license.

One a technical level, the core of this dataset is a simple [RDF](https://www.w3.org/RDF/) file that contains instances of licenses, such as the two listed above, that is then used to generate other RDF files in multiple formats and an HTML version of the information, held in a single HTML file. URIs assigned to the licenses resolve to either the RDF files or the HTML file allowing both humans and machines to resolve a license given its URI. It is expected that this dataset will eventually be delivered using a Linked Data API or some other system that allows for more sophisticated URI resolution.

## License
This repository is licensed under Creative Commons 4.0 International. See the [LICENSE deed](LICENSE) for details.

## Contacts
Creator:
**Nicholas Car**  
*Senior Experimental Scientist*  
CSIRO Land & Water, Environmental Informatics Group
Brisbane, Qld, Australia
<nicholas.car@csiro.au>
<http://orcid.org/0000-0002-8742-7730>
