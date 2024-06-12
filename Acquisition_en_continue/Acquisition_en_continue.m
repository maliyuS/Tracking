% Acquisition
steps = 2e9;
Span = 5e6;

rx = sdrrx('Pluto', 'OutputDataType', 'double', 'SamplesPerFrame', 2^24); % Connexion USB par défaut

%% Configure Rx Channels
% rx_lo
rx.CenterFrequency = 2.25e9;

% rx_mode
rx.GainSource = "AGC Fast Attack";  % For signals with rapidly changing power levels

% OutputDataType
rx.OutputDataType = "double";

% Sampling
rx.SamplesPerFrame = 2^18; %Buffer_size
rx.BasebandSampleRate = 30e6; %Sample_rate

%% Configure Spectrum Analyzer
FrequencySpan = "span-and-center-frequency";

sa = dsp.SpectrumAnalyzer('SampleRate', rx.BasebandSampleRate, 'FrequencySpan',  FrequencySpan, 'Span', Span);

%% Configure TimeScope
samplesPerStep = rx.SamplesPerFrame / rx.BasebandSampleRate;
AxesScaling = 'auto';

ts = timescope('SampleRate', rx.BasebandSampleRate, 'TimeSpan', samplesPerStep / 1e6 , 'AxesScaling', AxesScaling);

%% Start spectrum and analyser
for k=1 : steps

    data = rx();

    sa(data);
    ts(data);

    release(ts);
    pause(1);

end
