from kipoi_gwas import regulatory_features


rule fetch_regulatry_features:
    output:
        '{fdir}/bar_dgff_regulation_combo_type.png'
    run:
        regulatory_features.run(wildcards.ddir)

