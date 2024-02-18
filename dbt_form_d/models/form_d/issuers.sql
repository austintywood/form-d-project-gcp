{{ config(materialized='table') }}

select      ACCESSIONNUMBER                     as accession_number
            , case
                when IS_PRIMARYISSUER_FLAG = 'YES' then true
                when IS_PRIMARYISSUER_FLAG = 'NO' then false
            end                                 as is_primary_issuer_flag
            , ISSUER_SEQ_KEY                    as issuer_seq_key
            , regexp_replace(CIK, r'^0+', '')   as cik
            , ENTITYNAME                        as entity_name
            , STREET1                           as street_1
            , STREET2                           as street_2
            , CITY                              as city
            , STATEORCOUNTRY                    as state_or_country
            , STATEORCOUNTRYDESCRIPTION         as state_or_country_description
            , ZIPCODE                           as zip_code
            , ISSUERPHONENUMBER                 as issuer_phone_number
            , JURISDICTIONOFINC                 as jurisdiction_of_inc
            , ISSUER_PREVIOUSNAME_1             as issuer_previous_name_1
            , ISSUER_PREVIOUSNAME_2             as issuer_previous_name_2
            , ISSUER_PREVIOUSNAME_3             as issuer_previous_name_3
            , EDGAR_PREVIOUSNAME_1              as edgar_previous_name_1
            , EDGAR_PREVIOUSNAME_2              as edgar_previous_name_2
            , EDGAR_PREVIOUSNAME_3              as edgar_previous_name_3
            , ENTITYTYPE                        as entity_type
            , ENTITYTYPEOTHERDESC               as entity_type_other_desc
            , YEAROFINC_TIMESPAN_CHOICE         as year_of_inc_timespan_choice
            , YEAROFINC_VALUE_ENTERED           as year_of_inc_value_entered
from        {{ source('raw', 'issuers')}}
