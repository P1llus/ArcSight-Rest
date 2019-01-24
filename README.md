# Arcsight Logger REST Development SDK

DEPRECATED - This release will be the last for this repository(v2.0). All new versions can be followed
on the repository created for all future arcsight content on (https://github.com/arcsight-unofficial).

At a later date, a redirection will be added for this project towards the new one.

The newest version, 2.0, is a total rewrite of the old SDK, with better documentation,
fixing old issues, and adhere more to the PEP coding standards. This is not backward compatible
with older releases.

This is a python library to interact with the REST API that is offered on the Arcsight Logger

### Installation:

Install library with pip:
```sh
$ pip install loggersdk
```
Import the library in your script or application:
```python
import loggersdk
```

### Examples:

There is now new unofficial documentation for utilizing the ArcSight Logger API:

[ArcSight Logger API Documentation, web based](https://github.com/arcsight-unofficial/arcsight-logger-api-documentation)

[ArcSight Logger API Examples using Postman](https://github.com/arcsight-unofficial/arcsight-logger-api-examples)

[ArcSight Logger API SDK implementation example](https://github.com/arcsight-unofficial/arcsight-logger-api-sdkexample)

[ArcSight Logger API SDK](https://github.com/arcsight-unofficial/arcsight-logger-api-sdk)

### Optional Parameters for API requests:
Only the mandatory options is implemented for each function call, all optional arguments for each API call can be found in the above web based documentation and can be supplied as the last arguments when creating an instance of the function.
This is because each function with optional parameters also accepts unlimited kwargs as the last scope item.
An example of this integration can be found in the SDK implementation example above.

### Support:
This SDK is not officially supported by Micro Focus, for any issues please post a issue on the github issue page or ask on
the [ArcSight Community forums](https://community.softwaregrp.com/t5/ArcSight-User-Discussions/bd-p/arcsight-discussions)
