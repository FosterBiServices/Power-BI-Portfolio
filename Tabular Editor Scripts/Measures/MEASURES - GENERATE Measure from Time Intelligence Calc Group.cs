/*
 * Generate time intelligence measures based on calculation group items alredy created
 *
 * Author: Benoit Fedit, https://urldefense.com/v3/__https://datakuity.com/__;!!FfJJDeFhVu5QqWLN!beVlOkl9fw31QybZqL_Lgl-SRC8mTKl8Vx_WFdwkaGKoZfdppXJCogCBn39rGb7RYSsh2TUaqIvvaJGuNX78q7xDXw$  
 *
 * You must have created the calculation group items beforehand (see link below)
 * https://urldefense.com/v3/__https://docs.microsoft.com/en-us/analysis-services/tabular-models/calculation-groups?view=asallproducts-allversions__;!!FfJJDeFhVu5QqWLN!beVlOkl9fw31QybZqL_Lgl-SRC8mTKl8Vx_WFdwkaGKoZfdppXJCogCBn39rGb7RYSsh2TUaqIvvaJGuNX4oXwEeUQ$ 
 * To add more measure simply copy/paste the YTD script and replace YTD by your calculation item name
 */


 // For each selected measure create MOM; MOM%, PM, PQ, MTD, QTD, YTD, PY, PY MTD, PY QTD, PY YTD, QOQ, QOQ%, YOY, YOY% measures
foreach(var m in Selected.Measures) {
    
    // MTD
    m.Table.AddMeasure(
    m.Name + " MTD",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"MTD\")",    
    m.DisplayFolder                                        // Display Folder
    );
    
    // MOM
    m.Table.AddMeasure(
    m.Name + " MOM",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"MOM\")",    
    m.DisplayFolder                                        // Display Folder
    );
    
    // MOM%
    m.Table.AddMeasure(
    m.Name + " MOM%",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"MOM%\")",    
    m.DisplayFolder                                        // Display Folder
    ).FormatString = "0.0 %";
    
    // PM
    m.Table.AddMeasure(
    m.Name + " PM",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"PM\")",    
    m.DisplayFolder                                        // Display Folder
    );
    
    // PQ
    m.Table.AddMeasure(
    m.Name + " PQ",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"PQ\")",    
    m.DisplayFolder                                        // Display Folder
    );
    
    // QTD
    m.Table.AddMeasure(
    m.Name + " QTD",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"QTD\")",    
    m.DisplayFolder                                        // Display Folder
    );
    
    // YTD
    m.Table.AddMeasure(
    m.Name + " YTD",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"YTD\")",    
    m.DisplayFolder                                        // Display Folder
    );
    
    // PY
    m.Table.AddMeasure(
    m.Name + " PY",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"PY\")",    
    m.DisplayFolder                                        // Display Folder
    );
    
    // PY MTD
    m.Table.AddMeasure(
    m.Name + " PY MTD",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"PY MTD\")",    
    m.DisplayFolder                                        // Display Folder
    );
    
    // PY QTD
    m.Table.AddMeasure(
    m.Name + " PY QTD",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"PY QTD\")",    
    m.DisplayFolder                                        // Display Folder
    );
    
    // PY YTD
    m.Table.AddMeasure(
    m.Name + " PY YTD",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"PY YTD\")",    
    m.DisplayFolder                                        // Display Folder
    );
    
    // YOY
    m.Table.AddMeasure(
    m.Name + " YOY",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"YOY\")",    
    m.DisplayFolder                                        // Display Folder
    );
    
    // QOQ
    m.Table.AddMeasure(
    m.Name + " QOQ",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"QOQ\")",    
    m.DisplayFolder                                        // Display Folder
    );
        
    // YOY%
    m.Table.AddMeasure(
    m.Name + " YOY%",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"YOY%\")",    
    m.DisplayFolder                                        // Display Folder
    ).FormatString = "0.0 %";
        
    // QOQ%
    m.Table.AddMeasure(
    m.Name + " QOQ%",                                       // Name
    "Calculate(" + m.DaxObjectName + ", 'Time Intelligence'[Time Calculation]=\"QOQ%\")",    
    m.DisplayFolder                                        // Display Folder
    ).FormatString = "0.0 %";
}