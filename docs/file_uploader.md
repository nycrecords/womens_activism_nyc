# File upload process

This was done with the goal of changing as little things as possible
so it may not be the best solution, but as painless as it can.

## Previous method

The old method required users to upload images manually to a file host
and then paste the URL into an input element connected to
WTForms. There is a column in the database for storing the URL to the
image and the rest of the codebase just refers to the image through
that.

## New method

For the sake of maintainability and simplicity, a file uploader was
written from scratch. It uses the blob
[slice](https://developer.mozilla.org/en-US/docs/Web/API/Blob/slice)
method to split the file into chunks that are asynchronously uploaded
with Ajax calls.

There is a new upload-file view that is the core of this new method of
file upload. It temporarily writes the new file locally and uploads
the file to a staging folder in azure. It then deletes the file
locally and returns a URL to the file blob on azure.

Then the frontend relays this URL to a hidden element tied with
WTForms, which leads the URL to be back in the main view. Inside the
main view, the blob is copied from the staging folder to its final
folder. The database now holds the name of the blob rather than a URL
to the file.

Finally, when the image needs to be displayed, an SAS key with 1 hour
expriration time is acquired and the image is shown through that.
