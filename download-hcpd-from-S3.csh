#!/bin/tcsh

# =======================================================================================================================
# DOWNLOAD HCP-D DATA to BOX
# Written by Taylor J. Keding (tjkeding@gmail.com)
# Last Updated: 06.04.20
# =======================================================================================================================

# Set directory paths
set box = "/Users/tjkeding/Box"
set HCPDBox_cmd = "${box}/BRAVE\ Research\ Center/BRAVE\ Trainees/Datasets/HCPD"
set HCPDBox = "${box}/BRAVE Research Center/BRAVE Trainees/Datasets/HCPD"
set files = "${box}/Neuroscience PhD/MRI Projects/HTC Preprocessing/S3 File Lists/HCP/HCPD_allFiles_s3.csv"
set fileList = `cat "${files}"`

set iter = 1
# Iterate through file paths
foreach file($fileList)

  echo "Working on file $iter"

  # Calculate the number of parent and child directories in the current path
  set currDirs = `echo "$file" | awk 'BEGIN{FS="/"}{for (i=1; i<=NF; i++) print $i}'`
  set len = ${#currDirs}
  @ endLen = $len
  @ len = $len

  # Get only the file name
  set justFile = $currDirs[$endLen]

  # Remove file name from current path
  set currPath = `echo "$file" | cut -d/ -f-$len`

  # Remove s3 prefix from current path
  set finalPath = `echo "$currPath" | cut -c 6-`

  # Make directory on Box
  echo ".....Creating new directory on Box"
  mkdir -p "${HCPDBox}/${finalPath}"

  # If file doesn't already exist, download it from s3
  echo ".....Transfering files"

  set string1 = "aws s3 cp"
  set string2 = `echo "$file"`#| sed 's/.$//'`
  set string3 = "${HCPDBox_cmd}"/"${finalPath}/"

  set currCommand="$string1 $string2 $string3"
  set currOutFile = "${HCPDBox}"/"${finalPath}"/"${justFile}"

  #set formOutFile = `echo "$currOutFile" | sed 's/.$//'`
  set formOutFile = "$currOutFile"

  if (! -e "$formOutFile") then
    eval $currCommand
    if (-e "$formOutFile") then
      echo "...SUCCESS!"
    else
      echo "...FAILED!"
    endif
  else
    echo "...FILE ALREADY EXISTS!"
  endif

  @ iter = $iter + 1

end # for each file in fileList
