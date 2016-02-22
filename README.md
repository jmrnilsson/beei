# Bee.i

## Description
A shell client for fetching beer data.

## Licensing information
The software licensed under MIT.

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
