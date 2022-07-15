-- 1. We will use the CSV loader to read the file, lets ´import´ it first
define CSVLoader org.apache.pig.piggybank.storage.CSVLoader();

-- 2. Load the order2.csv file. We will use the columns as provided on Moodle.
orders = LOAD '/hadoop/orders.csv' USING CSVLoader(',') AS (
	game_id : int,
        unit_id : int, 
        unit_order : chararray, 
        location : chararray, 
        target : chararray, 
        target_dest : chararray, 
        success : int, 
        reason : chararray, 
        turn_num : int
);

-- 3. We want to filter the orders by the target Holland
filtered_orders = FILTER orders BY target == 'Holland';

-- 4. Then, group the orders by location
grouped_orders = FOREACH(GROUP filtered_orders by location) GENERATE group as location, MAX(filtered_orders.(target)) as target, COUNT($1) as c;

-- 5. Finally, sort alphabetically 
sorted_orders = ORDER grouped_orders BY location ASC;

-- 6. Output the results
DUMP sorted_orders
