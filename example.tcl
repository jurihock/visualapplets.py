CreateDesign "Example" "mE5-MA-VCLx"
SetDesignProperty "ProjectName" "Example"
SetDesignProperty "Version" ""
SetDesignProperty "Description" ""
CreateModule "HierarchicalBox" "Process0/Example" "1" "1" "86" "123"
CreateModule "BRANCH" "Process0/Example/Branch" "0" "3" "86" "43"
CreateModule "IS_GreaterThan" "Process0/Example/Condition" "0" "0" "206" "123"
CreateModule "CONST" "Process0/Example/Value" "0" "0" "206" "203"
CreateModule "IF" "Process0/Example/Decision" "0" "0" "326" "43"
ConnectModules "Process0/Example" "INBOUND#I000" "Process0/Example/Branch" "I"
ConnectModules "Process0/Example/Branch" "O000" "Process0/Example/Decision" "I000"
ConnectModules "Process0/Example/Branch" "O001" "Process0/Example/Condition" "I"
ConnectModules "Process0/Example/Condition" "O" "Process0/Example/Decision" "Condition000"
ConnectModules "Process0/Example/Branch" "O002" "Process0/Example/Value" "I"
ConnectModules "Process0/Example/Value" "O" "Process0/Example/Decision" "ElseI"
ConnectModules "Process0/Example/Decision" "O" "Process0/Example" "OUTBOUND#O000"
SetLinkParam "Process0/Example/Branch" "I" "Bit Width" "16"
SetLinkParam "Process0/Example/Branch" "I" "Arithmetic" "signed"
SetLinkParam "Process0/Example/Value" "O" "Bit Width" "16"
SetLinkParam "Process0/Example/Value" "O" "Arithmetic" "signed"
SetModuleParam "Process0/Example/Condition" "Number" "0"
SetModuleParam "Process0/Example/Value" "Value" "0"
