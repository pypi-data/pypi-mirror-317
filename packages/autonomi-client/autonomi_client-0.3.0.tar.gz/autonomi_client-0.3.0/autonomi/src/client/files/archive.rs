// Copyright 2024 MaidSafe.net limited.
//
// This SAFE Network Software is licensed to you under The General Public License (GPL), version 3.
// Unless required by applicable law or agreed to in writing, the SAFE Network Software distributed
// under the GPL Licence is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied. Please review the Licences for the specific language governing
// permissions and limitations relating to use of the SAFE Network Software.

use std::{
    collections::HashMap,
    path::{Path, PathBuf},
};

use ant_networking::target_arch::{Duration, SystemTime, UNIX_EPOCH};

use crate::{
    client::{
        data::{DataMapChunk, GetError, PutError},
        payment::PaymentOption,
    },
    Client,
};
use bytes::Bytes;
use serde::{Deserialize, Serialize};
use thiserror::Error;

/// Private archive data map, allowing access to the [`PrivateArchive`] data.
pub type PrivateArchiveAccess = DataMapChunk;

#[derive(Error, Debug, PartialEq, Eq)]
pub enum RenameError {
    #[error("File not found in archive: {0}")]
    FileNotFound(PathBuf),
}

/// Metadata for a file in an archive. Time values are UNIX timestamps.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Metadata {
    /// When the file was (last) uploaded to the network.
    pub uploaded: u64,
    /// File creation time on local file system. See [`std::fs::Metadata::created`] for details per OS.
    pub created: u64,
    /// Last file modification time taken from local file system. See [`std::fs::Metadata::modified`] for details per OS.
    pub modified: u64,
    /// File size in bytes
    pub size: u64,
}

impl Metadata {
    /// Create a new metadata struct with the current time as uploaded, created and modified.
    pub fn new_with_size(size: u64) -> Self {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or(Duration::from_secs(0))
            .as_secs();

        Self {
            uploaded: now,
            created: now,
            modified: now,
            size,
        }
    }
}

/// Directory structure mapping filepaths to their data maps and metadata.
///
/// The data maps are stored within this structure instead of uploading them to the network, keeping the data private.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Default)]
pub struct PrivateArchive {
    map: HashMap<PathBuf, (DataMapChunk, Metadata)>,
}

impl PrivateArchive {
    /// Create a new emtpy local archive
    /// Note that this does not upload the archive to the network
    pub fn new() -> Self {
        Self {
            map: HashMap::new(),
        }
    }

    /// Rename a file in an archive
    /// Note that this does not upload the archive to the network
    pub fn rename_file(&mut self, old_path: &Path, new_path: &Path) -> Result<(), RenameError> {
        let (data_addr, mut meta) = self
            .map
            .remove(old_path)
            .ok_or(RenameError::FileNotFound(old_path.to_path_buf()))?;
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or(Duration::from_secs(0))
            .as_secs();
        meta.modified = now;
        self.map.insert(new_path.to_path_buf(), (data_addr, meta));
        debug!("Renamed file successfully in the private archive, old path: {old_path:?} new_path: {new_path:?}");
        Ok(())
    }

    /// Add a file to a local archive
    /// Note that this does not upload the archive to the network
    pub fn add_file(&mut self, path: PathBuf, data_map: DataMapChunk, meta: Metadata) {
        self.map.insert(path.clone(), (data_map, meta));
        debug!("Added a new file to the archive, path: {:?}", path);
    }

    /// List all files in the archive
    pub fn files(&self) -> Vec<(PathBuf, Metadata)> {
        self.map
            .iter()
            .map(|(path, (_, meta))| (path.clone(), meta.clone()))
            .collect()
    }

    /// List all data addresses of the files in the archive
    pub fn addresses(&self) -> Vec<DataMapChunk> {
        self.map
            .values()
            .map(|(data_map, _)| data_map.clone())
            .collect()
    }

    /// Iterate over the archive items.
    ///
    /// Returns an iterator over ([`PathBuf`], [`DataMapChunk`], [`Metadata`])
    pub fn iter(&self) -> impl Iterator<Item = (&PathBuf, &DataMapChunk, &Metadata)> {
        self.map
            .iter()
            .map(|(path, (data_map, meta))| (path, data_map, meta))
    }

    /// Get the underlying map
    pub fn map(&self) -> &HashMap<PathBuf, (DataMapChunk, Metadata)> {
        &self.map
    }

    /// Deserialize from bytes.
    pub fn from_bytes(data: Bytes) -> Result<PrivateArchive, rmp_serde::decode::Error> {
        let root: PrivateArchive = rmp_serde::from_slice(&data[..])?;

        Ok(root)
    }

    /// Serialize to bytes.
    pub fn to_bytes(&self) -> Result<Bytes, rmp_serde::encode::Error> {
        let root_serialized = rmp_serde::to_vec(&self)?;
        let root_serialized = Bytes::from(root_serialized);

        Ok(root_serialized)
    }
}

impl Client {
    /// Fetch a [`PrivateArchive`] from the network
    pub async fn archive_get(
        &self,
        addr: PrivateArchiveAccess,
    ) -> Result<PrivateArchive, GetError> {
        let data = self.data_get(addr).await?;
        Ok(PrivateArchive::from_bytes(data)?)
    }

    /// Upload a [`PrivateArchive`] to the network
    pub async fn archive_put(
        &self,
        archive: &PrivateArchive,
        payment_option: PaymentOption,
    ) -> Result<PrivateArchiveAccess, PutError> {
        let bytes = archive
            .to_bytes()
            .map_err(|e| PutError::Serialization(format!("Failed to serialize archive: {e:?}")))?;
        let result = self.data_put(bytes, payment_option).await;
        debug!("Uploaded private archive {archive:?} to the network and address is {result:?}");
        result
    }
}
