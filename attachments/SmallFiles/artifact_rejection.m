% file loading
%nev = openNEV();
%chID = [38, 39, 141];
%stimCh = openNSx('C:\Users\emmae\PennNeurosurgery Dropbox\Beauchamp Laboratory\PennEMU\EMU_Data\PAV073\iEEGData\macro\031\raw\PAV073_Datafile_031.ns5', 'uv', 'channels', chID);

% double check the channel label
%stimCh.ElectrodesInfo.Label
%plot(stimCh.Data)
%hold on

% we do not want to analyze data at the stimulating electrode
interestCh = openNSx('/Users/beauchamplab/Downloads/PAV075_Datafile_024.ns5', 'uv', 'channels', 88);

% plot raw data
plot(interestCh.Data)
hold on

% Load additional channels for bipolar referencing
refCh1 = openNSx('/Users/beauchamplab/Downloads/PAV075_Datafile_024.ns5', 'uv', 'channels', 90);

% bipolar rereferencing
bipolarData = interestCh.Data-refCh1.Data; % in this case 88-90
plot(bipolarData)
hold on

% % figure out timing of pulse locations: plot sync (from events channel)
% for i = 197:208
%     sync = openNSx('C:\Users\emmae\PennNeurosurgery Dropbox\Beauchamp Laboratory\PennEMU\EMU_Data\PAV076\iEEGData\macro\003\raw\PAV076_Datafile_003.ns5', 'uv', 'channels', i);
%     disp(i)
%     disp(sync.ElectrodesInfo.Label)
% end

sync = openNSx('/Users/beauchamplab/Downloads/PAV075_Datafile_024.ns5', 'uv', 'channels', 171);

% clean sync pulse
sync.Data(sync.Data > 100) = 5e3;

% edge or findpeaks
% test this code...also try using edge
% [~,stimOnset] = findpeaks(sync.Data, 'MinPeakHeight',4000, 'MinPeakDistance',1e5);
% sync_reverse = fliplr(sync.Data);
% [~,stimOffset] = findpeaks(sync_reverse, 'MinPeakHeight',4000, 'MinPeakDistance',1e5);
% stimOffset = length(sync.Data) - stimOffset + 1;
% stimOffset = fliplr(stimOffset);

%first derivative method
thresh = 4000;
pulse = sync.Data > thresh;
stimOnset  = find(diff(pulse) ==  1);
stimOffset = find(diff(pulse) == - 1) + 1;

% pulses = min(numel(stimOnset), numel(stimOffset));
% stimOnset = stimOnset(1:pulses);
% stimOffset = stimOffset(1:pulses);

plot(sync.Data)
xline(stimOnset)
xline(stimOffset)

fs = interestCh.MetaTags.SamplingFreq;
freq = 200;
%dur = 0.5; % duration of pulse train
%artifact_samps = round(dur * freq); % calculate number of samples for artifact duration

win = fs / freq;

loc = [];
for n = 1:numel(stimOnset)
    loc = [loc linspace(stimOnset(n), stimOffset(n) - win, 100)];
end

snips = [];
for n = 1:numel(loc) % do 2:numel instead of 1:numel if the amplifier recovery on the first trial looks really different
    snips(:, n) = bipolarData(1, loc(n) : loc(n) + (win-0.5)); % do win-0.5 if still getting edge of artifact
end

plot(snips);

psnips = snips;
psnips(1:25, :) = nan;

plot(psnips);
hold on

% find average to build template
psnips = detrend(psnips, 0, 'omitnan');
template = mean(psnips, 2, 'omitnan');

plot(template, LineWidth=2);

template = template';

% template subtraction
cleanData = bipolarData;
for n = 1:numel(loc)
    cleanData(loc(n) : loc(n) + (win-0.5)) = cleanData(loc(n) : loc(n) + (win-0.5)) - template;
end

plot(cleanData)
hold on

% interpolate --> takes any point that is NaN and replaces it with moving mean
interp = movmean(cleanData, 150, 'omitnan');
cleanData(isnan(cleanData)) = interp(isnan(cleanData));

% filtfilt goes backwards and forwards, bc filt induces a phase shift and the reverse shifts it back
lpf = 250;
normed = lpf / (fs/2);
[b, a] = butter(4, normed, 'low');
lpData = filtfilt(b, a, cleanData);

plot(lpData)

% downsample to 2K
dsFs = 2000;
dsData = lpData(1:fs/dsFs:end);

% convert to .mat files
save('PAV075_Datafile_024_ch088.mat', 'dsData');