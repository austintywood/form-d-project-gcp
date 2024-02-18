{{ config(materialized='table') }}

select      ACCESSIONNUMBER                     as accession_number
            , RECIPIENT_SEQ_KEY                 as recipient_seq_key
            , RECIPIENTNAME                     as recipient_name
            , RECIPIENTCRDNUMBER                as recipient_crd_number
            , ASSOCIATEDBDNAME                  as associated_bd_name
            , ASSOCIATEDBDCRDNUMBER             as associated_bd_crd_number
            , STREET1                           as street_1
            , STREET2                           as street_2
            , CITY                              as city
            , STATEORCOUNTRY                    as state_or_country
            , STATEORCOUNTRYDESCRIPTION         as state_or_country_description
            , ZIPCODE                           as zip_code
            , STATES_OR_VALUE_LIST              as states_or_value_list
            , DESCRIPTIONS_LIST                 as descriptions_list
            , cast(FOREIGNSOLICITATION as bool) as foreign_solicitation
from        {{ source('raw', 'recipients')}}
