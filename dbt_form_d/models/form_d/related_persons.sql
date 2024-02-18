{{ config(materialized='table') }}

select      ACCESSIONNUMBER                 as accession_number
            , RELATEDPERSON_SEQ_KEY         as related_person_seq_key
            , FIRSTNAME                     as first_name
            , MIDDLENAME                    as middle_name
            , LASTNAME                      as last_name
            , STREET1                       as street_1
            , STREET2                       as street_2
            , CITY                          as city
            , STATEORCOUNTRY                as state_or_country
            , STATEORCOUNTRYDESCRIPTION     as state_or_country_description
            , ZIPCODE                       as zip_code
            , RELATIONSHIP_1                as relationship_1
            , RELATIONSHIP_2                as relationship_2
            , RELATIONSHIP_3                as relationship_3
            , RELATIONSHIPCLARIFICATION     as relationship_clarification
from        {{ source('raw', 'related_persons')}}
