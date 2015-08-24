function documentNode = build(strikes, idealSourceName, modelSourceName, autodelimitRows, idealSourceDetails, modelSourceDetails, visualisationDetails)

numBells = max([strikes.bell]);

documentNode = com.mathworks.xml.XMLUtils.createDocument('transcription');

rootNode = documentNode.getDocumentElement;
rootNode.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance');
rootNode.setAttribute('xsi:schemaLocation', 'http://drichards2.github.io/toast-visualiser/xsd/enhanced-strike-definition.xsd');
rootNode.setAttribute('version', '1');

datasources = documentNode.createElement('dataSources');
sim_datasource = documentNode.createElement('dataSource');
sim_datasource_name = documentNode.createElement('name');
sim_datasource_name.appendChild(documentNode.createTextNode(idealSourceName));
% sim_datasource_version = documentNode.createElement('version');
% sim_datasource_version.appendChild(documentNode.createTextNode(VERSION));
% sim_datasource_comment = documentNode.createElement('comment');
% sim_datasource_comment.appendChild(documentNode.createTextNode('Matlab ringing simulator - fantastic things are about to happen'));
sim_datasource.appendChild( sim_datasource_name );
datasources.appendChild(sim_datasource);


if ~strcmp(idealSourceName, modelSourceName)
    sim_datasource = documentNode.createElement('dataSource');
    sim_datasource_name = documentNode.createElement('name');
    sim_datasource_name.appendChild(documentNode.createTextNode(modelSourceName));
    % sim_datasource_version = documentNode.createElement('version');
    % sim_datasource_version.appendChild(documentNode.createTextNode(VERSION));
    % sim_datasource_comment = documentNode.createElement('comment');
    % sim_datasource_comment.appendChild(documentNode.createTextNode('Matlab ringing simulator - fantastic things are about to happen'));
    sim_datasource.appendChild( sim_datasource_name );
    datasources.appendChild(sim_datasource);
end

rootNode.appendChild(datasources);

% renderlayers = documentNode.createElement('renderLayers');
% visualisation = documentNode.createElement('visualisation');
% visualisation_name = documentNode.createElement('name');
% visualisation_name.appendChild(documentNode.createTextNode('Matlab Ringing Simulator'));
% visualisation_description = documentNode.createElement('description');
% visualisation_description.appendChild(documentNode.createTextNode('Nothing to see here'));
% visualisation_prioritylist = documentNode.createElement('priorityList');
% visualisation_prioritylist_source = documentNode.createElement('source');
% visualisation_prioritylist_source.appendChild(documentNode.createTextNode(sourceName));
% visualisation_prioritylist.appendChild(visualisation_prioritylist_source);

% visualisation.appendChild(visualisation_name);
% visualisation.appendChild(visualisation_description);
% visualisation.appendChild(visualisation_prioritylist);
% renderlayers.appendChild(visualisation);

% rootNode.appendChild(renderlayers);

strikedata  = documentNode.createElement('strikeData');
for runstrikes = 1:length(strikes)
    if mod(runstrikes, numBells) == 1
        if autodelimitRows
            rowDelimiter = documentNode.createElement('rowDelimiter');
            rowDelimiter.setAttribute('source', idealSourceName);
            strikedata.appendChild(rowDelimiter);
        end
    end
    strike_node = documentNode.createElement('strike');
    strike_bell = documentNode.createElement('bell');
    strike_bell.appendChild(documentNode.createTextNode(sprintf('%d', strikes(runstrikes).bell)));
    strike_node.appendChild( strike_bell );
    strike_original = documentNode.createElement('original');
    strike_original.appendChild(documentNode.createTextNode(sprintf('%.3f', strikes(runstrikes).actual_time)));
    strike_original.setAttribute('source', modelSourceName);
    strike_node.appendChild( strike_original );
    
    if isfield( strikes, 'ideal_time' )
        strike_modelout = documentNode.createElement('modelOutput');
        strike_modelout.setAttribute('source', idealSourceName);
        strike_modelout_time = documentNode.createElement('time');
        strike_modelout_time.appendChild(documentNode.createTextNode(sprintf('%.3f', strikes(runstrikes).ideal_time)));
        strike_modelout.appendChild( strike_modelout_time );
        strike_node.appendChild( strike_modelout );
    end
    
    strikedata.appendChild( strike_node );
end

rootNode.appendChild(strikedata);
