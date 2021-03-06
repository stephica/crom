[![Build Status](https://travis-ci.org/thegetty/crom.svg?branch=master)](https://travis-ci.org/thegetty/crom) [![Coverage Status](https://coveralls.io/repos/github/thegetty/crom/badge.svg?branch=master)](https://coveralls.io/github/thegetty/crom?branch=master)

# Cromulent

A Python library to make creation of CIDOC CRM easier by mapping classes/predicates to python objects/properties, thereby making the CRM "CRoMulent", a Simpsons neologism for "acceptable" or "fine".  

## Status: Alpha

The core vocabulary loading functionality is reasonably stable. The vocabulary section is expanding as we find new, useful terms to include and will likely change to instead be loaded separately from configurations.

The code is actively being developed and compability breaking changes are thus to be expected as we use it in various projects across The J Paul Getty Trust, and beyond.

## How to Use It

### Basic Usage

Import the classes from the model module. As the classes are dynamically generated, they're not in the code but will be there once the `build_classes` function has been called.

```python
from cromulent.model import factory, Group
g1 = Group("Organization")
g2 = Group("Department")
g1.member = g2
print factory.toString(g1, compact=False)
```

### Vocabulary

```python
from cromulent.model import factory
from cromulent.vocab import Height
h = Height()
h.value = 6
print factory.toString(h, compact=False)
```

### Tricks and Gotchas

* Assigning to the same property repeatedly does NOT overwrite the value, instead it appends. To overwrite a value, instead set it to a false value first.

### Factory settings

There are quite a few settings for how the module works, which are managed by a `factory` object.  

URI and File System Configuration:
* `base_url` The base url on to which to append any slug given when an object is created
* `base_dir` The base directory into which to write files, via factory.toFile()
* `filename_extension` The extension to use on files written via toFile(), defaults to ".json"
* `default_lang` The code for the default language to use on text values
* `context_uri` The URI to use for `@context` in the JSON-LD serialization
* `context_json` The parsed JSON object of the context from which the prefixes are derived
* `full_names` Should the serialization use the full CRM names for classes and properties instead of the more readable ones defined in the mapping, defaults to False
* `prefixes` A dictionary of prefix to URI for URIs to compress down to `prefix:slug` format
* `prefixes_rev` The reverse of the prefixes dictionary
* `pipe_scoped_contexts` A convenience setting for generating documentation, where properties that map to the same JSON output are represented as `short_name|full_name` to be post-processed.
* `json_indent` How many spaces should each level of indentation be when serializing to a human readable form, defaults to 2
* `id_type_label` Should the id, type and label properties all be used when serializing resources that have already been processed, defaults to True
* `elasticsearch_compatible` Despite JSON-LD 1.0 compaction rules, should a single URI be represented as {"@id": "URI"} rather than just "URI", to make the resulting JSON compatible with elasticsearch and similar JSON processing engines. Defaults to False.
* `serialize_all_resources` NOT YET IMPLEMENTED. If true, then all resources will be serialized separately, not just the top level resource.

Model Validation and Generation:
* `materialize_inverses` Should the inverse relationships be set automatically, defaults to False
* `validate_properties` Should the model be validated at run time when setting properties, defaults to True  (this allows you to save processing time once you're certain your code does the right thing)
* `validate_properties` Should the properties be validated as being part of the model at all
* `validate_profile` Should the profile of which terms should be used be validated
* `process_multiplicity` Should properties that allow multiple values always be an array
* `validate_range` Should the object be validated that it is legal to be the value of the property
* `auto_assign_id` Should a URI be autogenerated and assigned, defaults to True
* `auto_id_type` The method by which the URI is generated, taken from the following values:
  * "int" (just increment an integer in a single value space)
  * "int-per-type" (increment an integer, with a separate value space per class)
  * "int-per-segment" (increment an integer, with a separate value space per URI segment associated with a class)
  * "uuid" (just use UUIDs everywhere)

Internal:
* `debug_level` Settings for debugging errors and warnings, defaults to "warn"
* `log_stream` An object implementing the stream API to write log messages to, defaults to sys.stderr

Note that factories are NOT thread safe during serialization. A property on the factory is used to maintain which objects have been serialized already, to avoid infinite recursion in a cyclic graph. Create a new factory object per thread if necessary.


## How it Works

At import time, the library parses the vocabulary data file (data/crm_vocab.tsv) and creates Python classes in the module's global scope from each of the defined RDF classes.  The names of the classes are intended to be easy to use and remember, not necessarily identical to the CRM ontology's names. It also records the properties that can be used with that class, and at run time checks whether the property is defined and that the value fits the defined range.

## Hacking 

You can change the mapping by tweaking `utils/vocab_reader.py` and rerunning it to build a new TSV input file.  See also the experimental code for loading completely different ontologies.

