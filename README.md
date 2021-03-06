# Bee.i

1.

1.
# Description
A shell client for fetching beer data.

## Licensing information
The software licensed under MIT.

## Running
Use `make setup`, `make run` and `make test-integration`

## Querying

Once data fetched querying is possible with e.g. `grep` and `jq`.


    # Typical example, look for a beer named Bell
    make run && cat beers.json | grep -i Bell

    # Open the first beer in a browser
    cat beers.json | grep 'st-eriks' | sed -e 's/"href": "/ /g' -e 's/"/ /g' -e 's/,/ /g' | head -n 1 | xargs open

    # Deep diving into the stores. Find all product names
    ls . | xargs cat ./logs/ | grep -i name | awk '{print $2}' | sort | uniq

    # Show a little before and after
    ls . | xargs cat ./logs/ | grep -A 50 -B 50 some_brewery

    # Extract value with jq
    cat brewerydb-fd3ee35373c7e9b6a29a657e3d8d6aedbba21b23.json | jq '[. | {name: .data[].name, style: .data[].style.name, abv: .data[].abv}]'

    # Extract values in batch
    ls -la . | grep brewerydb | awk '$5 > 46 {print "./"$9}' | xargs cat | jq '[{name: .data[].name, style: .data[].style.name, abv: .data[].abv}]'

    # Sort list all unique names
    (cd logs; ls -1 . | grep rate | xargs cat | grep name | sed -e 's/    "name": "/ /g' -e 's/",/ /g' | uniq | sort)

    # Create a backup
    tar -zcvf ./config/2013-04-01.tar.gz ./logs

    # Check age of local storage
    ls -la logs/ | grep rate

    # Check specific sources
    (cd logs/; ls -1 | grep 'rate\|bo' | xargs cat)
