{{ config(materialized='table') }}

select      ACCESSIONNUMBER                 as accession_number
            , SIGNATURE_SEQ_KEY             as signature_seq_key
            , ISSUERNAME                    as issuer_name
            , SIGNATURENAME                 as signature_name
            , NAMEOFSIGNER                  as name_of_signer
            , SIGNATURETITLE                as signature_title
            , cast(SIGNATUREDATE as date)   as signature_date
from        {{ source('raw', 'signatures')}}
