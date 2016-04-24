# Bee.i

## Description
A shell client for fetching beer data.

## Licensing information
The software licensed under MIT.

## Running
Use `make setup`, `make run` and `make test-integration`

## Querying

Once data fetched querying is possible with e.g. `grep` and `jq`.


    # Find all product names
    ls . | xargs cat ./logs/ | grep ProductName | awk '{print $2}' | sort | uniq

    # Type info before and after
    ls . | xargs cat ./logs/ | grep -A 50 -B 50 some_brewery

    # Extract value with jq
    cat brewerydb-fd3ee35373c7e9b6a29a657e3d8d6aedbba21b23.json | jq '[. | {name: .data[].name, style: .data[].style.name, abv: .data[].abv}]'

    # Extract values in batch
    ls -la . | grep brewerydb | awk '$5 > 46 {print "./"$9}' | xargs cat | jq '[{name: .data[].name, style: .data[].style.name, abv: .data[].abv}]'

    # Check age of local storage
    ls -la logs/ | grep rate

    # Sort list all unique names
    (cd logs; ls -1 . | grep rate | xargs cat | grep name | sed -e 's/    "name": "/ /g' -e 's/",/ /g' | uniq | sort)

    # Create a backup
    tar -zcvf ./config/2013-04-01.tar.gz ./logs

    # Check any source for non-unicode characters
    (cd logs/; ls -1 | grep 'rate\|bo' | xargs cat)

    # Look for a specific item
    (cd logs/; ls -1 | xargs cat | grep 'Crystal')